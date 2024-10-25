from flask import abort, redirect, render_template, request, url_for
from flask import Blueprint, flash, current_app
from src.model.generic.operations import document_operations
from src.model.generic.operations import document_types_operations
from src.web.handlers.check_permission import permission_required
from src.model.riders.operations import disability_diagnosis_operations
from src.model.riders.operations import disability_type_operations
from src.model.riders.operations import family_allowance_type_operations
from src.model.riders.operations import pension_type_operations
from src.model.riders.operations import rider_operations
from src.model.riders.operations import school_operations
from src.model.riders.operations import work_day_operations
from src.model.riders.operations import school_operations
from src.model.generic.operations import locality_operations
from src.model.generic.operations import province_operations
from src.model.generic.operations import address_operations
from src.model.generic.operations import work_proposal_operations
from src.model.generic.operations import sede_operations
from src.model.horses.operations import horse_operations
from src.model.employees.operations import employee_operations
from uuid import uuid4
from src.model.riders.tables.rider import Rider
from src.model.generic.tables.address import Address
from src.model.riders.tables.school import School
from src.model.riders.tables.disability_diagnosis import DisabilityDiagnosis
import re

bp = Blueprint("rider", __name__, url_prefix="/JyA")

@bp.route("/")
@permission_required('rider_index')
def index():
    localities = locality_operations.list_localitys()
    localities = [locality.name for locality in localities]
    provinces = province_operations.list_provinces()
    provinces = [province.name for province in provinces]

    page = request.args.get('page')
    start_ascending = request.args.get('ascending') is None
    sort_attr = request.args.get('sort_attr') or "inserted_at"
    search_attr = request.args.get('search_attr') or "name"
    search_value = request.args.get('search_value') or ""

    start_sort_attr = sort_attr if sort_attr else ""
    start_search_attr = search_attr if search_attr else ""
    start_search_val = search_value if search_value else ""
    search_attr_esp = to_spanish(start_search_attr)
    pages = 1
    riders = []

    try:
        if not page:
            page = 1
        else:
            page = int(page)

        data = rider_operations.get_riders_filtered_list(page=page, sort_attr=sort_attr, ascending=start_ascending, search_attr=search_attr,
                                                                search_value=search_value)

        riders = data[0]
        pages = data[1]
    except Exception as e:
        print(e)
        flash("Uso inválido de parametros, no se pudo aplicar el filtro", "error")
        page = 0

    return render_template("riders/index.html", pages=pages, riders=riders, localities=localities, provinces=provinces, start_sort_attr=start_sort_attr,
                            start_search_attr=start_search_attr, search_attr_esp=search_attr_esp, start_search_val=start_search_val,
                            start_ascending=(not start_ascending), start_page=page)

@bp.get("/nuevo")
@permission_required('rider_create')
def new():
    riders = rider_operations.list_riders()
    localitys = locality_operations.list_localitys()
    provinces = province_operations.list_provinces()
    disability_diagnosis = disability_diagnosis_operations.list_disability_diagnosis()
    disability_types = disability_type_operations.list_disability_type()
    family_allowance_types = family_allowance_type_operations.list_family_allowance_types()
    pension_types = pension_type_operations.list_pension_types()
    schools = school_operations.list_schools()
    work_proposals = work_proposal_operations.list_work_proposals()
    work_days = work_day_operations.list_work_days()
    sedes = sede_operations.list_sedes()
    horses = horse_operations.list_horses()
    employees = employee_operations.list_employees()

    dnis = [rider.dni for rider in riders]
    affiliate_numbers = [rider.affiliate_number for rider in riders]

    return render_template(
        "riders/new.html", riders=riders, localitys=localitys, provinces=provinces, disability_diagnosis=disability_diagnosis,
        disability_types=disability_types, family_allowance_types=family_allowance_types, pension_types=pension_types, schools=schools,
        work_proposals=work_proposals, work_days=work_days, sedes=sedes, horses=horses, employees=employees, dnis=dnis, affiliate_numbers=affiliate_numbers)
    
@bp.post("/create")
@permission_required('rider_create')
def create():
    params = request.form

    rider_data = {
        "name": params.get("name"),
        "surname": params.get("surname"),
        "dni": params.get("dni"),
        "age": params.get("age"),
        "birth_date": params.get("birth_date"),
        "birth-locality": params.get("birth-locality"),
        "birth-province": params.get("birth-province"),
        "street": params.get("street"),
        "number": params.get("number"),
        "apartment": params.get("apartment"),
        "current-locality": params.get("current-locality"),
        "current-province": params.get("current-province"),
        "phone": params.get("phone"),
        "emergency-contact-name": params.get("emergency-contact-name"),
        "emergency-phone": params.get("emergency-phone"),
        "has-scholarship": params.get("has-scholarship") == 'on',
        "disable-certificate": params.get("disable-certificate") == 'on',
        "disability-diagnosis": params.get("disability-diagnosis"),
        "new-disability": params.get("new-disability"),
        "has-family-allowance": params.get("has-family-allowance") == 'on',
        "family-allowance-type": params.get("family-allowance-type"),
        "receives-pension": params.get("receives-pension") == 'on',
        "pension-type": params.get("pension-type"),
        "disability-type": params.get("disability-type"),
        "health-insurance": params.get("health-insurance"),
        "affiliate-number": params.get("affiliate-number"),
        "has-guardianship": params.get("has-guardianship") == 'on',
        "school-id": params.get("school-id"),
        "school-name": params.get("school-name"),
        "school-address": params.get("school-address"),
        "school-phone": params.get("school-phone"),
        "current-grade": params.get("current-grade"),
        "professionals": params.get("professionals"),
        "guardian1-name": params.get("guardian1-name"),
        "guardian1-surname": params.get("guardian1-surname"),
        "guardian1-dni": params.get("guardian1-dni"),
        "guardian1-street": params.get("guardian1-street"),
        "guardian1-number": params.get("guardian1-number"),
        "guardian1-apartment": params.get("guardian1-apartment"),
        "guardian1-locality": params.get("guardian1-locality"),
        "guardian1-province": params.get("guardian1-province"),
        "guardian1-phone": params.get("guardian1-phone"),
        "guardian1-email": params.get("guardian1-email"),
        "guardian1-educational-level": params.get("guardian1-educational-level"),
        "guardian1-occupation": params.get("guardian1-occupation"),
        "guardian1-relationship": params.get("guardian1-relationship"),
        "guardian2-name": params.get("guardian2-name"),
        "guardian2-surname": params.get("guardian2-surname"),
        "guardian2-dni": params.get("guardian2-dni"),
        "guardian2-street": params.get("guardian2-street"),
        "guardian2-number": params.get("guardian2-number"),
        "guardian2-apartment": params.get("guardian2-apartment"),
        "guardian2-locality": params.get("guardian2-locality"),
        "guardian2-province": params.get("guardian2-province"),
        "guardian2-phone": params.get("guardian2-phone"),
        "guardian2-email": params.get("guardian2-email"),
        "guardian2-educational-level": params.get("guardian2-educational-level"),
        "guardian2-occupation": params.get("guardian2-occupation"),
        "guardian2-relationship": params.get("guardian2-relationship"),
        "work-proposal-id": params.get("work-proposal-id"),
        "active": params.get("active") == 'on',
        "sede-id": params.get("sede-id"),
        "teacher-id": params.get("teacher-id"),
        "horse-conductor-id": params.get("horse-conductor-id"),
        "horse-id": params.get("horse-id"),
        "track-assistant-id": params.get("track-assistant-id"),
    }

    check_dni = rider_operations.get_rider_by_dni(rider_data["dni"])
    check_affiliate_number = rider_operations.get_rider_by_affiliate_number(rider_data["affiliate_number"])

    if check_dni or check_affiliate_number:
        flash("Lo lamentamos, ha habido un error inesperado", "error")
        return redirect((url_for("employee.new")))
    
    try:
        address = address_operations.create_address(rider_data["street"], rider_data["number"], rider_data["apartment"])
        addressGuardian1 = address_operations.create_address(rider_data["guardian1-street"], rider_data["guardian1-number"], rider_data["guardian1-apartment"])
        addressGuardian2 = address_operations.create_address(rider_data["guardian2-street"], rider_data["guardian2-number"], rider_data["guardian2-apartment"])

        if (rider_data["school-name"] == "Otro"):
            school = School(rider_data["school-name"], rider_data["school-adress"], rider_data["school-phone"])
            school.id = rider.school_id
            school_operations.create_school(school)

        if (rider_data["disable-certificate"] and rider_data["disability-diagnosis"] == "Otro"):
            disability = DisabilityDiagnosis(params.get("new-disability"))
            disability.id = rider.disability_diagnosis_id
            disability_diagnosis_operations.create_disability_diagnosis(disability)

        rider_operations.create_rider(
            name = rider_data["name"],
            last_name = rider_data["surname"],
            dni = rider_data["dni"],
            age = rider_data["age"],
            birth_date = rider_data["birth_date"],
            birth_locality_id = rider_data["birth-locality"],
            birth_province_id = rider_data["birth-province"],
            address_id = rider.address_id,
            current_locality_id = rider_data["current-locality"],
            current_province_id = rider_data["current-province"],
            phone = rider_data["phone"],
            emergency_contact_name = rider_data["emergency-contact-name"],
            emergency_contact_phone = rider_data["emergency-phone"],
            has_scholarship = rider_data["has-scholarship"],
            has_disability_certificate = rider_data["disable-certificate"],
            disability_diagnosis_id = rider.disability_diagnosis_id,
            receives_family_allowance = rider_data["has-family-allowance"],
            family_allowance_type_id = rider_data["family-allowance-type"],
            receives_pension = rider_data["receives-pension"],
            pension_type_id = rider_data["pension-type"],
            disability_type_id = rider_data["disability-type"],
            health_insurance = rider_data["health-insurance"],
            affiliate_number = rider_data["affiliate-number"],
            has_guardianship = rider_data["has-guardianship"],
            school_id = rider.school_id,
            current_grade = rider_data["current-grade"],
            attending_professionals = rider_data["professionals"],
            work_proposal_id = rider_data["work-proposal-id"],
            active = rider_data["active"],
            sede_id = rider_data["sede-id"],
            teacher_id = rider_data["teacher-id"],
            horse_conductor_id = rider_data["horse-conductor-id"],
            horse_id = rider_data["horse-id"],
            track_assistant_id = rider_data["track-assistant-id"],
            
            guardian1_name = rider_data["guardian1-name"],
            guardian1_last_name = rider_data["guardian1-surname"],
            guardian1_dni = rider_data["guardian1-dni"],
            guardian1_address_id = rider.guardian1_address_id,
            guardian1_locality_id = rider_data["guardian1-locality"],
            guardian1_province_id = rider_data["guardian1-province"],
            guardian1_phone = rider_data["guardian1-phone"],
            guardian1_email = rider_data["guardian1-email"],
            guardian1_education_level = rider_data["guardian1-educational-level"],
            guardian1_occupation = rider_data["guardian1-occupation"],
            guardian1_relationship = rider_data["guardian1-relationship"],
            
            guardian2_name = rider_data["guardian2-name"],
            guardian2_last_name = rider_data["guardian2-surname"],
            guardian2_dni = rider_data["guardian2-dni"],
            guardian2_address_id = rider.guardian1_address_id,
            guardian2_locality_id = rider_data["guardian2-locality"],
            guardian2_province_id = rider_data["guardian2-province"],
            guardian2_phone = rider_data["guardian2-phone"],
            guardian2_email = rider_data["guardian2-email"],
            guardian2_education_level = rider_data["guardian2-educational-level"],
            guardian2_occupation = rider_data["guardian2-occupation"],
            guardian2_relationship = rider_data["guardian2-relationship"]
        )
    except:
        flash("Uso inválido de parametros, no se pudo actualizar al usuario", "error")
        return redirect(url_for("home"))

    return redirect(url_for("employee.index"))

@bp.get("/<int:id>")
@permission_required('rider_show')
def show(id):
    rider = rider_operations.get_rider(id)
    if rider:
        #Traido las cosas que voy a necesitar
        riders = rider_operations.list_riders()
        localitys = locality_operations.list_localitys()
        provinces = province_operations.list_provinces()
        documents = document_operations.list_documents_by_rider_id(rider.id)
        disability_diagnosis = disability_diagnosis_operations.list_disability_diagnosis()
        disability_types = disability_type_operations.list_disability_type()
        family_allowance_types = family_allowance_type_operations.list_family_allowance_types()
        pension_types = pension_type_operations.list_pension_types()
        schools = school_operations.list_schools()
        work_proposals = work_proposal_operations.list_work_proposals()
        work_days = work_day_operations.list_work_days()
        sedes = sede_operations.list_sedes()
        horses = horse_operations.list_horses()
        employees = employee_operations.list_employees()
        #Aca estaría bueno crear varias listas según el rol para que en la selección se ofrezcan los que trabajan de eso, pero no queda muy claro en las jobs positions
        
        document_types = document_types_operations.list_document_type()
        start_document_type = request.args.get('start-document-type') or ""

        rider.address = address_operations.get_addres(rider.address_id)
        rider.guardian1_address = address_operations.get_addres(rider.guardian1_address_id)
        rider.guardian2_address = address_operations.get_addres(rider.guardian2_address_id)
        school = schools[rider.school_id - 1]
        
        mode = request.args.get("mode", "general")
        
        dnis = [rider.dni for rider in riders]
        affiliate_numbers = [rider.affiliate_number for rider in riders]
        dnis.remove(rider.dni)
        affiliate_numbers.remove(rider.affiliate_number)

        return render_template("riders/show.html", rider=rider, localitys=localitys, provinces=provinces, disability_diagnosis=disability_diagnosis, disability_types = disability_types, family_allowance_types=family_allowance_types, pension_types=pension_types, schools=schools, work_proposals=work_proposals, work_days=work_days, sedes=sedes, horses=horses, employees=employees, school=school, dnis=dnis, affiliate_numbers=affiliate_numbers, documents=documents, mode=mode)
    else:
        return abort(404)

@bp.post("/<int:id>/update")
@permission_required('rider_update')
def update(id):
    real_id = int(id)
    params = request.form
    riders = rider_operations.list_riders()

    rider_data = {
        "name": params.get("name"),
        "surname": params.get("surname"),
        "dni": params.get("dni"),
        "age": params.get("age"),
        "birth_date": params.get("birth_date"),
        "birth-locality": params.get("birth-locality"),
        "birth-province": params.get("birth-province"),
        "street": params.get("street"),
        "number": params.get("number"),
        "apartment": params.get("apartment"),
        "current-locality": params.get("current-locality"),
        "current-province": params.get("current-province"),
        "phone": params.get("phone"),
        "emergency-contact-name": params.get("emergency-contact-name"),
        "emergency-phone": params.get("emergency-phone"),
        "has-scholarship": params.get("has-scholarship") == 'on',
        "disable-certificate": params.get("disable-certificate") == 'on',
        "disability-diagnosis": params.get("disability-diagnosis"),
        "new-disability": params.get("new-disability"),
        "has-family-allowance": params.get("has-family-allowance") == 'on',
        "family-allowance-type": params.get("family-allowance-type"),
        "receives-pension": params.get("receives-pension") == 'on',
        "pension-type": params.get("pension-type"),
        "disability-type": params.get("disability-type"),
        "health-insurance": params.get("health-insurance"),
        "affiliate-number": params.get("affiliate-number"),
        "has-guardianship": params.get("has-guardianship") == 'on',
        "school-id": params.get("school-id"),
        "school-name": params.get("school-name"),
        "school-address": params.get("school-address"),
        "school-phone": params.get("school-phone"),
        "current-grade": params.get("current-grade"),
        "professionals": params.get("professionals"),
        "guardian1-name": params.get("guardian1-name"),
        "guardian1-surname": params.get("guardian1-surname"),
        "guardian1-dni": params.get("guardian1-dni"),
        "guardian1-street": params.get("guardian1-street"),
        "guardian1-number": params.get("guardian1-number"),
        "guardian1-apartment": params.get("guardian1-apartment"),
        "guardian1-locality": params.get("guardian1-locality"),
        "guardian1-province": params.get("guardian1-province"),
        "guardian1-phone": params.get("guardian1-phone"),
        "guardian1-email": params.get("guardian1-email"),
        "guardian1-educational-level": params.get("guardian1-educational-level"),
        "guardian1-occupation": params.get("guardian1-occupation"),
        "guardian1-relationship": params.get("guardian1-relationship"),
        "guardian2-name": params.get("guardian2-name"),
        "guardian2-surname": params.get("guardian2-surname"),
        "guardian2-dni": params.get("guardian2-dni"),
        "guardian2-street": params.get("guardian2-street"),
        "guardian2-number": params.get("guardian2-number"),
        "guardian2-apartment": params.get("guardian2-apartment"),
        "guardian2-locality": params.get("guardian2-locality"),
        "guardian2-province": params.get("guardian2-province"),
        "guardian2-phone": params.get("guardian2-phone"),
        "guardian2-email": params.get("guardian2-email"),
        "guardian2-educational-level": params.get("guardian2-educational-level"),
        "guardian2-occupation": params.get("guardian2-occupation"),
        "guardian2-relationship": params.get("guardian2-relationship"),
        "work-proposal-id": params.get("work-proposal-id"),
        "active": params.get("active") == 'on',
        "sede-id": params.get("sede-id"),
        "teacher-id": params.get("teacher-id"),
        "horse-conductor-id": params.get("horse-conductor-id"),
        "horse-id": params.get("horse-id"),
        "track-assistant-id": params.get("track-assistant-id"),
    }
 
    try:
        rider = rider_operations.get_rider(real_id)

        if not rider:
            flash("Lo lamentamos, ha habido un error inesperado", "error")
            return redirect((url_for("home")))

        dnis = [rider.dni for rider in riders]
        affiliate_numbers = [rider.affiliate_number for rider in riders]
        
        dnis.remove(rider.dni)
        affiliate_numbers.remove(rider.affiliate_number)

        if rider.dni in dnis or rider.affiliate_number in affiliate_numbers:
            flash("Lo lamentamos, ha habido un error inesperado", "error") #Aca otro mensaje quizas sea ofrecer informacion personal de otro
            return redirect((url_for("rider.show", id=rider.id)))

        # Actualizar address
        address = Address(rider_data["street"], rider_data["number"], rider_data["apartment"])
        address.id = rider.address_id
        address_operations.update_address(address)

        #Actualizar address del tutor 1
        addressGuardian1 = Address(rider_data["guardian1-street"], rider_data["guardian1-number"], rider_data["guardian1-apartment"])
        addressGuardian1.id = rider.guardian1_address_id
        address_operations.update_address(addressGuardian1)
        #Actualizar address del tutor 2
        addressGuardian2 = Address(rider_data["guardian2-street"], rider_data["guardian2-number"], rider_data["guardian2-apartment"])
        addressGuardian1.id = rider.guardian2_address_id
        address_operations.update_address(addressGuardian1)
        #Agrego escuela de ser necesario
        if (rider_data["school-name"] == "Otro"):
            school_operations.delete_school(rider.school_id)
            school = School(rider_data["school-name"], rider_data["school-adress"], rider_data["school-phone"])
            school.id = rider.school_id
            school_operations.create_school(school)

        #Agrego discapacidad de ser necesario
        if (rider_data["disable-certificate"] and rider_data["disability-diagnosis"] == "Otro"):
            disability_diagnosis_operations.delete_disability_diagnosis(rider.school_id)
            disability = DisabilityDiagnosis(params.get("new-disability"))
            disability.id = rider.disability_diagnosis_id
            disability_diagnosis_operations.create_disability_diagnosis(disability)


        rider = Rider(
            name = rider_data["name"],
            last_name = rider_data["surname"],
            dni = rider_data["dni"],
            age = rider_data["age"],
            birth_date = rider_data["birth_date"],
            birth_locality_id = rider_data["birth-locality"],
            birth_province_id = rider_data["birth-province"],
            address_id = rider.address_id,
            current_locality_id = rider_data["current-locality"],
            current_province_id = rider_data["current-province"],
            phone = rider_data["phone"],
            emergency_contact_name = rider_data["emergency-contact-name"],
            emergency_contact_phone = rider_data["emergency-phone"],
            has_scholarship = rider_data["has-scholarship"],
            has_disability_certificate = rider_data["disable-certificate"],
            disability_diagnosis_id = rider.disability_diagnosis_id,
            receives_family_allowance = rider_data["has-family-allowance"],
            family_allowance_type_id = rider_data["family-allowance-type"],
            receives_pension = rider_data["receives-pension"],
            pension_type_id = rider_data["pension-type"],
            disability_type_id = rider_data["disability-type"],
            health_insurance = rider_data["health-insurance"],
            affiliate_number = rider_data["affiliate-number"],
            has_guardianship = rider_data["has-guardianship"],
            school_id = rider.school_id,
            current_grade = rider_data["current-grade"],
            attending_professionals = rider_data["professionals"],
            work_proposal_id = rider_data["work-proposal-id"],
            active = rider_data["active"],
            sede_id = rider_data["sede-id"],
            teacher_id = rider_data["teacher-id"],
            horse_conductor_id = rider_data["horse-conductor-id"],
            horse_id = rider_data["horse-id"],
            track_assistant_id = rider_data["track-assistant-id"],
            
            guardian1_name = rider_data["guardian1-name"],
            guardian1_last_name = rider_data["guardian1-surname"],
            guardian1_dni = rider_data["guardian1-dni"],
            guardian1_address_id = rider.guardian1_address_id,
            guardian1_locality_id = rider_data["guardian1-locality"],
            guardian1_province_id = rider_data["guardian1-province"],
            guardian1_phone = rider_data["guardian1-phone"],
            guardian1_email = rider_data["guardian1-email"],
            guardian1_education_level = rider_data["guardian1-educational-level"],
            guardian1_occupation = rider_data["guardian1-occupation"],
            guardian1_relationship = rider_data["guardian1-relationship"],
            
            guardian2_name = rider_data["guardian2-name"],
            guardian2_last_name = rider_data["guardian2-surname"],
            guardian2_dni = rider_data["guardian2-dni"],
            guardian2_address_id = rider.guardian1_address_id,
            guardian2_locality_id = rider_data["guardian2-locality"],
            guardian2_province_id = rider_data["guardian2-province"],
            guardian2_phone = rider_data["guardian2-phone"],
            guardian2_email = rider_data["guardian2-email"],
            guardian2_education_level = rider_data["guardian2-educational-level"],
            guardian2_occupation = rider_data["guardian2-occupation"],
            guardian2_relationship = rider_data["guardian2-relationship"]
        )

        rider.id = real_id
        rider_operations.__update_rider__(rider)

        return redirect(url_for("rider.show", id=rider.id))
    except Exception as e:
        print(e)
        flash("Uso inválido de parametros, no se pudo actualizar al usuario", "error")
        return redirect(url_for("home"))

@bp.get("/<int:id>/delete")
@permission_required('rider_destroy')
def delete(id):
    rider_operations.delete_rider(id)
    return redirect(url_for("rider.index"))

# Utils functions
def is_valid_email(email :str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def to_spanish(attr: str) -> str:
    match attr:
        case "name":
            return "nombre"
        case "last_name":
            return "apellido"
        case _:
            return attr