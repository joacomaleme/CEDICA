from flask import abort, redirect, render_template, request, url_for
from flask import Blueprint, flash, current_app
from model.generic.operations import document_types_operations
from src.web.handlers.check_permission import permission_required
from src.model.employees.operations import employee_operations
from src.model.employees.operations import job_position_operations
from src.model.employees.operations import profession_operations
from src.model.generic.operations import document_operations
from src.model.generic.operations import locality_operations
from src.model.generic.operations import address_operations
from src.model.generic.tables.address import Address
from src.model.employees.tables.employee import Employee
from uuid import uuid4
import re

bp = Blueprint("employee", __name__, url_prefix="/empleados")

@bp.route("/")
@permission_required('employee_index')
def index():
    professions = profession_operations.list_professions()
    professions = [profession.name for profession in professions]
    job_positions = job_position_operations.list_job_positions()
    job_positions = [job_position.name for job_position in job_positions]

    page = request.args.get('page')
    start_ascending = request.args.get('ascending') is None
    sort_attr = request.args.get('sort_attr') or "inserted_at"
    search_attr = request.args.get('search_attr') or "email"
    search_value = request.args.get('search_value') or ""
    start_profession = request.args.get('profession') or ""

    start_sort_attr = sort_attr if sort_attr else ""
    start_search_attr = search_attr if search_attr else ""
    start_search_val = search_value if search_value else ""
    search_attr_esp = to_spanish(start_search_attr)
    pages = 1
    employees = []

    try:
        if not page:
            page = 1
        else:
            page = int(page)

        data = employee_operations.get_employees_filtered_list(page=page, sort_attr=sort_attr, ascending=start_ascending, search_attr=search_attr,
                                                                search_value=search_value, search_profession=start_profession)

        employees = data[0]
        pages = data[1]
    except Exception as e:
        flash("Uso inválido de parametros, no se pudo aplicar el filtro", "error")
        page = 0

    return render_template("employees/index.html", pages=pages, employees=employees, professions=professions, job_positions=job_positions, start_sort_attr=start_sort_attr,
                            start_search_attr=start_search_attr, search_attr_esp=search_attr_esp, start_search_val=start_search_val,
                            start_profession=start_profession, start_ascending=(not start_ascending), start_page=page)

@bp.get("/nuevo")
@permission_required('employee_new')
def new():
    employees = employee_operations.list_employees()
    professions = profession_operations.list_professions()
    job_positions = job_position_operations.list_job_positions()
    localitys = locality_operations.list_localitys()

    mails = [employee.email for employee in employees]
    dnis = [employee.dni for employee in employees]
    affiliate_numbers = [employee.affiliate_number for employee in employees]

    return render_template("employees/new.html", professions=professions, job_positions=job_positions, localitys=localitys,
                           mails=mails, dnis=dnis, affiliate_numbers=affiliate_numbers)

@bp.post("/create")
@permission_required('employee_create')
def create():
    params = request.form

    employee_data = {
        "name": params.get("name"),
        "surname": params.get("surname"),
        "dni": params.get("dni"),
        "street": params.get("street"),
        "number": params.get("number"),
        "apartment": params.get("apartment"),
        "email": params.get("email"),
        "locality": params.get("locality"),
        "phone": params.get("phone"),
        "profession_id": params.get("profession"),
        "job_position_id": params.get("job-position"),
        "emergency_contact_name": params.get("emergency-contact-name"),
        "emergency_contact_phone": params.get("emergency-contact-phone"),
        "obra_social": params.get("obra-social"),
        "affiliate_number": params.get("affiliate-number"),
        "is_volunteer": params.get("volunteer") != None,  # Convert to bool
        "start_date": params.get("start-date"),
        "end_date": params.get("end-date"),
    }

    check_dni = employee_operations.get_employee_by_dni(employee_data["dni"])
    check_mail = employee_operations.get_employee_by_email(employee_data["email"])
    check_affiliate_number = employee_operations.get_employee_by_affiliate_number(employee_data["affiliate_number"])

    if check_dni or check_mail or check_affiliate_number:
        flash("Lo lamentamos, ha habido un error inesperado", "error")
        return redirect((url_for("employee.new")))
    if (not is_valid_email(employee_data["email"])):
        flash("La dirección de mail ingresada no es válida", "error")
        return redirect((url_for("employee.new")))
    
    try:
        address = address_operations.create_address(employee_data["street"], employee_data["number"], employee_data["apartment"])

        employee_operations.create_employee(
            name = employee_data["name"],
            surname = employee_data["surname"],
            dni = employee_data["dni"],
            address_id = address.id,
            email = employee_data["email"],
            locality_id = employee_data["locality"],
            phone = employee_data["phone"],
            profession_id = employee_data["profession_id"],
            job_position_id = employee_data["job_position_id"],
            emergency_contact_name = employee_data["emergency_contact_name"],
            emergency_contact_phone = employee_data["emergency_contact_phone"],
            obra_social = employee_data["obra_social"],
            affiliate_number = employee_data["affiliate_number"],
            is_volunteer = employee_data["is_volunteer"],
            start_date = employee_data["start_date"],
            end_date = employee_data["end_date"],
        )
    except:
        flash("Uso inválido de parametros, no se pudo actualizar al usuario", "error")
        return redirect(url_for("home"))

    return redirect(url_for("employee.index"))

@bp.get("/<int:id>")
@permission_required('employee_show')
def show(id):
    employee = employee_operations.get_employee(id)
    if employee:
        employees = employee_operations.list_employees()
        localitys = locality_operations.list_localitys()
        professions = profession_operations.list_professions()
        job_positions = job_position_operations.list_job_positions()
        documents = document_operations.list_documents_by__employee_id(employee.id)
        
        # document_types = document_types_operations.list_document_type()
        # start_document_type = request.args.get('start-document-type') or ""
        mode = request.args.get("mode", "general")

        # Traigo el address y locality por ser una copia
        address = address_operations.get_addres(employee.address_id)
        locality = locality_operations.get_locality(employee.locality_id)

        employee.address = address
        employee.locality = locality

        mails = [employee.email for employee in employees]
        dnis = [employee.dni for employee in employees]
        affiliate_numbers = [employee.affiliate_number for employee in employees]
       
        mails.remove(employee.email)
        dnis.remove(employee.dni)
        affiliate_numbers.remove(employee.affiliate_number)
        
        return render_template("employees/show.html", employee=employee, localitys=localitys, professions=professions, job_positions=job_positions,
                                documents=documents, mails=mails, dnis=dnis, affiliate_numbers=affiliate_numbers,
                                mode=mode)
    else:
        return abort(404)

@bp.post("/<int:id>/update")
@permission_required('employee_update')
def update(id):
    real_id = int(id)
    params = request.form
    employees = employee_operations.list_employees()

    employee_data = {
        "name": params.get("name"),
        "surname": params.get("surname"),
        "dni": params.get("dni"),
        "street": params.get("street"),
        "number": params.get("number"),
        "apartment": params.get("apartment"),
        "email": params.get("email"),
        "locality": params.get("locality"),
        "phone": params.get("phone"),
        "profession_id": params.get("profession"),
        "job_position_id": params.get("job-position"),
        "emergency_contact_name": params.get("emergency-contact-name"),
        "emergency_contact_phone": params.get("emergency-contact-phone"),
        "obra_social": params.get("obra-social"),
        "affiliate_number": params.get("affiliate-number"),
        "is_volunteer": params.get("volunteer") != None,  # Convert to bool
        "start_date": params.get("start-date"),
        "end_date": params.get("end-date"),
    }

    try:
        employee = employee_operations.get_employee(real_id)

        if not employee:
            flash("Lo lamentamos, ha habido un error inesperado", "error")
            return redirect((url_for("home")))
        if (not is_valid_email(employee_data["email"])):
            flash("La dirección de mail ingresada no es válida", "error")
            return redirect((url_for("employee.show", id=employee.id)))

        mails = [employee.email for employee in employees]
        dnis = [employee.dni for employee in employees]
        affiliate_numbers = [employee.affiliate_number for employee in employees]
        
        mails.remove(employee.email)
        dnis.remove(employee.dni)
        affiliate_numbers.remove(employee.affiliate_number)

        if employee.email in mails or employee.dni in dnis or employee.affiliate_number in affiliate_numbers:
            flash("La dirección de mail ingresada no es válida", "error")
            return redirect((url_for("employee.show", id=employee.id)))

        # Actualizo el address
        address = Address(employee_data["street"], employee_data["number"], employee_data["apartment"])
        address.id = employee.address_id
        address_operations.update_address(address)

        employee = Employee(
            name = employee_data["name"],
            surname = employee_data["surname"],
            dni = employee_data["dni"],
            address_id = employee.address_id,
            email = employee_data["email"],
            locality_id = employee_data["locality"],
            phone = employee_data["phone"],
            profession_id = employee_data["profession_id"],
            job_position_id = employee_data["job_position_id"],
            emergency_contact_name = employee_data["emergency_contact_name"],
            emergency_contact_phone = employee_data["emergency_contact_phone"],
            obra_social = employee_data["obra_social"],
            affiliate_number = employee_data["affiliate_number"],
            is_volunteer = employee_data["is_volunteer"],
            start_date = employee_data["start_date"],
            end_date = employee_data["end_date"],
        )
        employee.id = real_id
        employee_operations.update_employee(employee)

        return redirect(url_for("employee.show", id=employee.id))
    except:
        flash("Uso inválido de parametros, no se pudo actualizar al usuario", "error")
        return redirect(url_for("home"))


@bp.get("/<int:id>/delete")
@permission_required('employee_destroy')
def delete(id):
    employee_operations.delete_employee(id)
    return redirect(url_for("employee.index"))

# Utils functions
def is_valid_email(email :str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def to_spanish(attr: str) -> str:
    match attr:
        case "name":
            return "nombre"
        case "surname":
            return "apellido"
        case _:
            return attr