from flask import abort, redirect, render_template, request, url_for
from flask import Blueprint, flash, current_app
from typing import List, Optional, Tuple
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
from datetime import datetime
import dns.resolver

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
    sort_attr = request.args.get('sort_attr') or "name"
    search_attr = request.args.get('search_attr') or "name"
    search_value = request.args.get('search_value') or ""

    if sort_attr not in ["name", "last_name"]:
        flash("Uso inválido de parametros, no se pudo aplicar el filtro", "error")
        sort_attr = "name"

    if search_attr not in ["name", "dni", "last_name", "professionals"]:
        flash("Uso inválido de parametros, no se pudo aplicar el filtro", "error")
        search_attr = "name"

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
    except:
        flash("Uso inválido de parametros, no se pudo aplicar el filtro", "error")
        page = 0
    
    data = rider_operations.get_riders_filtered_list(page=page, sort_attr=sort_attr, ascending=start_ascending, search_attr=search_attr,
                                                            search_value=search_value)

    riders = data[0]
    pages = data[1]

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

    res = check_rider_data(rider_data)
    if res[0] is False:
        flash(res[1], "error")
        return redirect(request.referrer)

    check_dni = rider_operations.get_rider_by_dni(rider_data["dni"])
    check_affiliate_number = rider_operations.get_rider_by_affiliate_number(rider_data["affiliate-number"])

    if check_dni or check_affiliate_number:
        flash("Lo lamentamos, ha habido un error inesperado", "error")
        return redirect((url_for("employee.new")))
    
    try:
        address = address_operations.create_address(rider_data["street"], rider_data["number"], rider_data["apartment"])
        addressGuardian1 = address_operations.create_address(rider_data["guardian1-street"], rider_data["guardian1-number"], rider_data["guardian1-apartment"])
        addressGuardian2 = address_operations.create_address(rider_data["guardian2-street"], rider_data["guardian2-number"], rider_data["guardian2-apartment"])

        if (rider_data["school-name"] == "Otro"):
            school = school_operations.create_school(rider_data["school-name"], rider_data["school-adress"], rider_data["school-phone"])
        else:
            school = school_operations.get_school(rider_data["school-id"])

        if (rider_data["disable-certificate"] and rider_data["disability-diagnosis"] == "Otro"):
            disability_diagnosis =  disability_diagnosis_operations.create_disability_diagnosis(params.get("new-disability"))
        else:
            disability_diagnosis = disability_diagnosis_operations.get_disability_diagnosis_by_diagnosis(rider_data["disability-diagnosis"])

        rider_operations.create_rider(
            name = rider_data["name"],
            last_name = rider_data["surname"],
            dni = rider_data["dni"],
            age = rider_data["age"],
            birth_date = rider_data["birth_date"],
            birth_locality_id = rider_data["birth-locality"],
            birth_province_id = rider_data["birth-province"],
            address_id = address.id,
            current_locality_id = rider_data["current-locality"],
            current_province_id = rider_data["current-province"],
            phone = rider_data["phone"],
            emergency_contact_name = rider_data["emergency-contact-name"],
            emergency_contact_phone = rider_data["emergency-phone"],
            has_scholarship = rider_data["has-scholarship"],
            has_disability_certificate = rider_data["disable-certificate"],
            disability_diagnosis_id = disability_diagnosis.id,
            receives_family_allowance = rider_data["has-family-allowance"],
            family_allowance_type_id = rider_data["family-allowance-type"],
            receives_pension = rider_data["receives-pension"],
            pension_type_id = rider_data["pension-type"],
            disability_type_id = rider_data["disability-type"],
            health_insurance = rider_data["health-insurance"],
            affiliate_number = rider_data["affiliate-number"],
            has_guardianship = rider_data["has-guardianship"],
            school_id = school.id,
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
            guardian1_address_id = addressGuardian1.id,
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
            guardian2_address_id = addressGuardian2.id,
            guardian2_locality_id = rider_data["guardian2-locality"],
            guardian2_province_id = rider_data["guardian2-province"],
            guardian2_phone = rider_data["guardian2-phone"],
            guardian2_email = rider_data["guardian2-email"],
            guardian2_education_level = rider_data["guardian2-educational-level"],
            guardian2_occupation = rider_data["guardian2-occupation"],
            guardian2_relationship = rider_data["guardian2-relationship"]
        )
    except Exception as e:
        print(e)
        flash("Uso inválido de parametros, no se pudo crear al usuario", "error")
        return redirect(url_for("home"))

    return redirect(url_for("rider.index"))

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
        
        types = document_types_operations.list_document_type()
        start_type = request.args.get('start-document-type') or ""

        page = request.args.get('page')
        start_ascending = request.args.get('ascending') is None
        sort_attr = request.args.get('sort_attr') or "upload_date"
        search_title = request.args.get('search_title') or ""
        mode = request.args.get("mode")
        if not mode or mode != "documents":
            mode = "general"

        pages = 1

        res = check_show_data(types, page, sort_attr, start_type)
        if res[0] is False:
            flash(res[1], "error")
            return redirect(request.referrer)

        page = 1 if not page else int(page)


        rider.address = address_operations.get_addres(rider.address_id)
        rider.guardian1_address = address_operations.get_addres(rider.guardian1_address_id)
        rider.guardian2_address = address_operations.get_addres(rider.guardian2_address_id)
        school = schools[rider.school_id - 1]
        
        dnis = [rider.dni for rider in riders]
        affiliate_numbers = [rider.affiliate_number for rider in riders]

        dnis.remove(rider.dni)
        affiliate_numbers.remove(rider.affiliate_number)
        

        data = document_operations.get_documents_filtered_list(documents=documents, page=page, sort_attr=sort_attr, ascending=start_ascending, search_title=search_title, search_type=start_type)

        documents = data[0]
        pages = data[1]

        return render_template("riders/show.html", rider=rider, localitys=localitys, provinces=provinces, disability_diagnosis=disability_diagnosis, disability_types = disability_types, family_allowance_types=family_allowance_types, pension_types=pension_types, schools=schools, work_proposals=work_proposals, work_days=work_days, sedes=sedes, horses=horses, employees=employees, school=school, dnis=dnis, affiliate_numbers=affiliate_numbers, documents=documents, mode=mode, pages=pages, startPage=page, start_ascending=(not start_ascending), sort_attr=sort_attr, search_title=search_title, start_type=start_type, types=types)
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

    res = check_rider_data(rider_data)
    if res[0] is False:
        flash(res[1], "error")
        return redirect(request.referrer)
 
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

def is_valid_email(email :str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def domain_exists(email:str):
    '''
    Valida que exista un servidor MX para la dirección de mail pasada por parametro. Retorna True si existe, false si no.
    '''
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return False

def is_valid_dni(dni: str) -> bool:
    pattern = r'^\d+$'
    return re.match(pattern, dni) is not None

def is_valid_phone(phone: str) -> bool:
    pattern = r'^[\d\-]+$'
    return re.match(pattern, phone) is not None

def is_valid_date(date_str: str) -> bool:
    try:
        # Intenta convertir la cadena de fecha en un objeto datetime con el formato 'YYYY-MM-DD'
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        # Si ocurre un error de conversión, la fecha no es válida
        return False

def to_spanish(attr: str) -> str:
    match attr:
        case "name":
            return "nombre"
        case "last_name":
            return "apellido"
        case _:
            return attr

def check_index_data(
        page: Optional[str],
        sort_attr: str,
        search_attr: str,
        search_value: str) -> Tuple[bool, str]:
    if (page and not isinstance(page, str)) or not isinstance(sort_attr, str) or not isinstance(search_attr, str) or not isinstance(search_value, str):
        return (False, "Algúno de los tipos de los parámetros es incorrecto.")
    if not sort_attr in ["inserted_at", "name", "last_name"]:
        return (False, "Atributo de ordenamiento incorrecto.")
    if not search_attr in ["dni", "name", "last_name", "professionals"]:
        return (False, "Atributo de busqueda incorrecto.")

    if page:
        try:
            int(page)
        except:
            return (False, "Tipo de pagina inválido.")
    
    return (True, "")

def check_show_data(
        types: List["DocumentType"],
        page: Optional[str],
        sort_attr: str,
        start_type: str) -> Tuple[bool, str]:
    if (page and not isinstance(page, str)) or not isinstance(sort_attr, str):
        return (False, "Algúno de los tipos de los parámetros es incorrecto.")
    #if not sort_attr in ["upload_date", "title"]:
        #return (False, "Atributo de ordenamiento incorrecto.")
    
    if page:
        try:
            int(page)
        except:
            return (False, "Tipo de pagina inválido.")

    return (True, "")

def check_rider_data(rider_data) -> Tuple[bool, str]:
    required_fields = [
        "name", "surname", "dni", "age", "birth_date", "birth-locality", "birth-province",
        "street", "number", "current-locality", "current-province", "phone",
        "emergency-contact-name", "emergency-phone", "disability-type", "health-insurance", "affiliate-number",
        "has-guardianship", "school-id", "current-grade", "professionals", "guardian1-name", "guardian1-surname", "guardian1-dni",
        "guardian1-street", "guardian1-number", "guardian1-locality",
        "guardian1-province", "guardian1-phone", "guardian1-email", "guardian1-educational-level",
        "guardian1-occupation", "guardian1-relationship", "guardian2-name", "guardian2-surname",
        "guardian2-dni", "guardian2-street", "guardian2-number",
        "guardian2-locality", "guardian2-province", "guardian2-phone", "guardian2-email",
        "guardian2-educational-level", "guardian2-occupation", "guardian2-relationship",
        "work-proposal-id", "sede-id", "teacher-id", "horse-conductor-id",
        "horse-id", "track-assistant-id"
    ]

    for field in required_fields:
        if not rider_data.get(field):
            return (False, f"Faltó rellenar un campo obligatorio {field}")

    if (rider_data["disability-diagnosis"] == "Otro"):
        if not rider_data.get("new-disability"):
            return (False, f"Faltó rellenar un campo obligatorio")
    if (rider_data["school-name"] == "Otro"):
        if not rider_data.get("school-address") or not rider_data.get("school-phone"):
            return (False, f"Faltó rellenar un campo obligatorio")
    if (rider_data["has-family-allowance"] is not None):
        if not rider_data.get("family-allowance-type"):
            return (False, f"Faltó rellenar un campo obligatorio")
    if (rider_data["disable-certificate"] is not None):
        if not rider_data.get("disability-diagnosis"):
            return (False, f"Faltó rellenar un campo obligatorio")
    if (rider_data["receives-pension"] is not None):
        if not rider_data.get("pension-type"):
            return (False, f"Faltó rellenar un campo obligatorio")

    if len(rider_data["name"]) > 100:
        return (False, "El nombre debe ser menor a 100 caracteres.")
    if len(rider_data["surname"]) > 100:
        return (False, "El apellido debe ser menor a 100 caracteres.")
    if len(rider_data["dni"]) > 16 or not is_valid_dni(rider_data["dni"]):
        return (False, "Error en el DNI ingresado.")
    if len(rider_data["age"]) > 3 or not rider_data["age"].isdigit():
        return (False, "La edad debe ser un número de hasta 3 dígitos.")
    if not is_valid_date(rider_data["birth_date"]):
        return (False, "Fecha de nacimiento no válida.")
    if len(rider_data["street"]) > 255:
        return (False, "La calle debe ser menor a 255 caracteres.")
    if len(rider_data["number"]) > 10:
        return (False, "El número debe ser menor a 10 caracteres.")
    if rider_data["apartment"] and len(rider_data["apartment"]) > 10:
        return (False, "El departamento debe ser menor a 10 caracteres.")
    if len(rider_data["phone"]) > 20 or not is_valid_phone(rider_data["phone"]):
        return (False, "Error en el teléfono ingresado.")
    if len(rider_data["emergency-contact-name"]) > 100:
        return (False, "El nombre del contacto de emergencia debe ser menor a 100 caracteres.")
    if len(rider_data["emergency-phone"]) > 20 or not is_valid_phone(rider_data["emergency-phone"]):
        return (False, "Error en el teléfono del contacto de emergencia.")
    if rider_data["disability-diagnosis"] == "Otro" and len(rider_data["new-disability"]) > 255:
        return (False, "La nueva discapacidad debe ser menor a 255 caracteres.")
    if len(rider_data["health-insurance"]) > 100:
        return (False, "La obra social debe ser menor a 100 caracteres.")
    if len(rider_data["affiliate-number"]) > 50:
        return (False, "El número de afiliado debe ser menor a 50 caracteres.")
    if (rider_data["school-name"] == "Otro") and len(rider_data["school-name"]) > 255:
        return (False, "El nombre de la escuela debe ser menor a 100 caracteres.")
    if (rider_data["school-name"] == "Otro") and len(rider_data["school-address"]) > 255:
        return (False, "La dirección de la escuela debe ser menor a 255 caracteres.")
    if (rider_data["school-name"] == "Otro") and (len(rider_data["school-phone"]) > 20 or not is_valid_phone(rider_data["school-phone"])):
        return (False, "Error en el teléfono de la escuela.")
    if len(rider_data["current-grade"]) > 50:
        return (False, "El grado actual debe ser menor a 50 caracteres.")
    if len(rider_data["professionals"]) > 255:
        return (False, "La lista de profesionales debe ser menor a 255 caracteres.")
    if len(rider_data["guardian1-name"]) > 100:
        return (False, "El nombre del primer tutor debe ser menor a 100 caracteres.")
    if len(rider_data["guardian1-surname"]) > 100:
        return (False, "El apellido del primer tutor debe ser menor a 100 caracteres.")
    if len(rider_data["guardian1-dni"]) > 16 or not is_valid_dni(rider_data["guardian1-dni"]):
        return (False, "Error en el DNI del primer tutor.")
    if len(rider_data["guardian1-street"]) > 255:
        return (False, "La calle del primer tutor debe ser menor a 255 caracteres.")
    if len(rider_data["guardian1-number"]) > 10:
        return (False, "El número de calle del primer tutor debe ser menor a 10 caracteres.")
    if len(rider_data["guardian1-apartment"]) > 10:
        return (False, "El departamento del primer tutor debe ser menor a 10 caracteres.")
    if len(rider_data["guardian1-phone"]) > 20 or not is_valid_phone(rider_data["guardian1-phone"]):
        return (False, "Error en el teléfono del primer tutor.")
    if len(rider_data["guardian1-email"]) > 100 or not is_valid_email(rider_data["guardian1-email"]) or not domain_exists(rider_data["guardian1-email"]):
        return (False, "Error en el correo electrónico del primer tutor.")
    if len(rider_data["guardian1-educational-level"]) > 50:
        return (False, "El nivel educativo del primer tutor debe ser menor a 50 caracteres.")
    if len(rider_data["guardian1-occupation"]) > 100:
        return (False, "La ocupación del primer tutor debe ser menor a 100 caracteres.")
    if len(rider_data["guardian1-relationship"]) > 20:
        return (False, "La relación con el primer tutor debe ser menor a 50 caracteres.")
    if len(rider_data["guardian2-name"]) > 100:
        return (False, "El nombre del primer tutor debe ser menor a 100 caracteres.")
    if len(rider_data["guardian2-surname"]) > 100:
        return (False, "El apellido del primer tutor debe ser menor a 100 caracteres.")
    if len(rider_data["guardian2-dni"]) > 16 or not is_valid_dni(rider_data["guardian2-dni"]):
        return (False, "Error en el DNI del primer tutor.")
    if len(rider_data["guardian2-street"]) > 255:
        return (False, "La calle del primer tutor debe ser menor a 255 caracteres.")
    if len(rider_data["guardian2-number"]) > 10:
        return (False, "El número de calle del primer tutor debe ser menor a 10 caracteres.")
    if len(rider_data["guardian2-apartment"]) > 10:
        return (False, "El departamento del primer tutor debe ser menor a 10 caracteres.")
    if len(rider_data["guardian2-phone"]) > 20 or not is_valid_phone(rider_data["guardian2-phone"]):
        return (False, "Error en el teléfono del primer tutor.")
    if len(rider_data["guardian2-email"]) > 100 or not is_valid_email(rider_data["guardian2-email"]) or not domain_exists(rider_data["guardian1-email"]):
        return (False, "Error en el correo electrónico del primer tutor.")
    if len(rider_data["guardian2-educational-level"]) > 50:
        return (False, "El nivel educativo del primer tutor debe ser menor a 50 caracteres.")
    if len(rider_data["guardian2-occupation"]) > 100:
        return (False, "La ocupación del primer tutor debe ser menor a 100 caracteres.")
    if len(rider_data["guardian2-relationship"]) > 20:
        return (False, "La relación con el primer tutor debe ser menor a 50 caracteres.")
    try:
        locality_ids = [locality.id for locality in locality_operations.list_localitys()]
        if not int(rider_data["birth-locality"]) in locality_ids:
            return (False, "ID de localidad inexistente.")
        if not int(rider_data["current-locality"]) in locality_ids:
            return (False, "ID de localidad inexistente.")
        if not int(rider_data["guardian1-locality"]) in locality_ids:
            return (False, "ID de localidad inexistente.")
        if not int(rider_data["guardian2-locality"]) in locality_ids:
            return (False, "ID de localidad inexistente.")
    except:
        return (False, "Error en alguna localidad ingresada.")
    
    try:
        province_ids = [province.id for province in province_operations.list_provinces()]
        if not int(rider_data["current-province"]) in province_ids:
            return (False, "ID de provincia inexistente.")
        if not int(rider_data["birth-province"]) in province_ids:
            return (False, "ID de provincia inexistente.")
        if not int(rider_data["guardian1-province"]) in province_ids:
            return (False, "ID de provincia inexistente.")
        if not int(rider_data["guardian2-province"]) in province_ids:
            return (False, "ID de provincia inexistente.")
    except:
        return (False, "Error en alguna provincia ingresada.")

    if (rider_data["disable-certificate"] is not None and rider_data["disability-diagnosis"] == "Otro"):
        try:
            disability_diagnosis = [disability_diagnosis.diagnosis for disability_diagnosis in disability_diagnosis_operations.list_disability_diagnosis()]
            if not (rider_data["disability-diagnosis"]) in disability_diagnosis:
                return (False, "Discapacidad inexistente.")
        except:
            return (False, "Error en la discapacidad ingresada.")

    if (rider_data["has-family-allowance"] is not None):
        try:
            family_allowance_type = [family_allowance_type.name for family_allowance_type in family_allowance_type_operations.list_family_allowance_types()]
            if not (rider_data["family-allowance-type"]) in family_allowance_type:
                return (False, "Tipo de asignación familiar inexistente.")
        except:
            return (False, "Error en el tipo de asignación familiar ingresado.")

    if (rider_data["receives-pension"] is not None):
        try:
            pension_type = [pension_type.name for pension_type in pension_type_operations.list_pension_types()]
            if not (rider_data["pension-type"]) in pension_type:
                return (False, "Tipo de pensión inexistente.")
        except:
            return (False, "Error en el tipo de pensión ingresado.")

    if (rider_data["school-name"] == "Otro"):
        try:
            school_ids = [school.id for school in school_operations.list_schools()]
            if not int(rider_data["school-id"]) in school_ids:
                return (False, "ID de escuela inexistente.")
        except:
            return (False, "Error en la escuela ingresada.")

    try:
        educational_levels = ["Primario", "Secundario", "Terciario", "Universitario"]
        if not (rider_data["guardian1-educational-level"]) in educational_levels:
            return (False, "Nivel educativo del primer tutor inexistente.")
        if not (rider_data["guardian2-educational-level"]) in educational_levels:
            return (False, "Nivel educativo del segundo tutor inexistente.")
    except:
        return (False, "Error en el nivel educativo del tutor ingresado.")

    try:
        work_proposal_ids = [work_proposal.id for work_proposal in work_proposal_operations.list_work_proposals()]
        if not int(rider_data["work-proposal-id"]) in work_proposal_ids:
            return (False, "ID de propuesta de trabajo inexistente.")
    except:
        return (False, "Error en la propuesta de trabajo ingresada.")

    try:
        sede_ids = [sede.id for sede in sede_operations.list_sedes()]
        if not int(rider_data["sede-id"]) in sede_ids:
            return (False, "ID de sede inexistente.")
    except:
        return (False, "Error en la sede ingresada.")

    try:
        employee_ids = [employee.id for employee in employee_operations.list_employees()]
        if not int(rider_data["teacher-id"]) in employee_ids:
            return (False, "ID de profesor inexistente.")
        if not int(rider_data["horse-conductor-id"]) in employee_ids:
            return (False, "ID de conductor del caballo inexistente.")
        if not int(rider_data["track-assistant-id"]) in employee_ids:
            return (False, "ID de auxiliar de pista inexistente.")
    except Exception as e:
        print(e)
        return (False, "Error en alguno de los empleados ingresados.")

    try:
        horse_ids = [horse.id for horse in horse_operations.list_horses()]
        if not int(rider_data["horse-id"]) in horse_ids:
            return (False, "ID de caballo inexistente.")
    except:
        return (False, "Error en el caballo ingresado.")

    return (True, "")