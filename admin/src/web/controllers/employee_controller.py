from datetime import datetime
from typing import List, Optional, Tuple
from flask import abort, redirect, render_template, request, url_for
from flask import Blueprint, flash
from model.generic.operations import document_types_operations
from src.model.riders.operations import rider_operations
from src.web.handlers.check_permission import permission_required
from src.model.employees.operations import employee_operations
from src.model.employees.operations import job_position_operations
from src.model.employees.operations import profession_operations
from src.model.generic.operations import document_operations
from src.model.generic.operations import locality_operations
from src.model.generic.operations import address_operations
from src.model.generic.tables.address import Address
from src.model.employees.tables.employee import Employee
import dns.resolver
import re

bp = Blueprint("employee", __name__, url_prefix="/empleados")

@bp.route("/")
@permission_required('employee_index')
def index():
    """
    Muestra una lista paginada de los empleados. Además permite aplicar filtros el resultado.
    """
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

    res = check_index_data(professions, page, sort_attr, search_attr, search_value, start_profession)
    if res[0] is False:
        flash(res[1], "error")
        return redirect(request.referrer)

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
    except:
        flash("Uso inválido de parametros, no se pudo aplicar el filtro", "error")
        page = 0

    return render_template("employees/index.html", pages=pages, employees=employees, professions=professions, job_positions=job_positions, start_sort_attr=start_sort_attr,
                            start_search_attr=start_search_attr, search_attr_esp=search_attr_esp, start_search_val=start_search_val,
                            start_profession=start_profession, start_ascending=(not start_ascending), startPage=page)

@bp.get("/nuevo")
@permission_required('employee_create')
def new():
    """
    Muestra el formulario para crear empleados nuevos.
    """
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
    """
    Permite crear un empleado nuevo, recibiendo los datos necesarios.
    """
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

    res = check_employee_data(employee_data)
    if res[0] is False:
        flash(res[1], "error")
        return redirect(request.referrer)
    
    check_dni = employee_operations.get_employee_by_dni(employee_data["dni"])
    check_mail = employee_operations.get_employee_by_email(employee_data["email"])
    check_affiliate_number = employee_operations.get_employee_by_affiliate_number(employee_data["affiliate_number"])

    if check_dni or check_mail or check_affiliate_number:
        flash("Lo lamentamos, ha habido un error inesperado", "error")
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
        documents = document_operations.list_documents_by_employee_id(id)
        types = document_types_operations.list_document_type()

        page = request.args.get('page')
        start_ascending = request.args.get('ascending') is None
        sort_attr = request.args.get('sort_attr') or "upload_date"
        search_title = request.args.get('search_title') or ""
        start_type = request.args.get('type') or ""
        mode = request.args.get("mode")
        if not mode or mode != "documents":
            mode = "general"

        pages = 1

        res = check_show_data(types, page, sort_attr, start_type)
        if res[0] is False:
            flash(res[1], "error")
            return redirect(request.referrer)

        page = 1 if not page else int(page)

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

        data = document_operations.get_documents_filtered_list(documents=documents, page=page, sort_attr=sort_attr, ascending=start_ascending, search_title=search_title,
                                                                search_type=start_type)

        documents = data[0]
        pages = data[1]

        # Checkeo si el empleado está relacionado con jinetes
        can_delete = not rider_operations.employee_exists(id)

        return render_template("employees/show.html", employee=employee, localitys=localitys, professions=professions, job_positions=job_positions,
                                documents=documents, mails=mails, dnis=dnis, affiliate_numbers=affiliate_numbers, mode=mode, pages=pages, startPage=page,
                                start_ascending=(not start_ascending), sort_attr=sort_attr, search_title=search_title, start_type=start_type, types=types, can_delete=can_delete)
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
 
    res = check_employee_data(employee_data)
    if res[0] is False:
        flash(res[1], "error")
        return redirect(request.referrer)

    try:
        employee = employee_operations.get_employee(real_id)

        if not employee:
            flash("Lo lamentamos, ha habido un error inesperado", "error")
            return redirect((url_for("home")))

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
    employee = employee_operations.get_employee(id)

    if not employee:
        flash("ID de empleado ingresado inexistente", "error")
        return redirect(request.referrer)
    
    if rider_operations.employee_exists(id):
        flash("No es posible eliminar este empleado", "error")
        return redirect(request.referrer)
    
    try:
        employee_operations.delete_employee(id)
    except:
        flash("Error al eliminar el usuario", "error")
        return redirect(request.referrer)

    return redirect(url_for("employee.index"))

# Utils functions
def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

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
    
def domain_exists(email: str) -> bool:
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return False

def to_spanish(attr: str) -> str:
    match attr:
        case "name":
            return "nombre"
        case "surname":
            return "apellido"
        case _:
            return attr

def check_index_data(
        professions: List["Profession"],
        page: Optional[str],
        sort_attr: str,
        search_attr: str,
        search_value: str,
        start_profession: str) -> Tuple[bool, str]:
    if (page and not isinstance(page, str)) or not isinstance(sort_attr, str) or not isinstance(search_attr, str) or not isinstance(search_value, str) or not isinstance(start_profession, str):
        return (False, "Algúno de los tipos de los parámetros es incorrecto.")
    if not sort_attr in ["inserted_at", "name", "surname"]:
        return (False, "Atributo de ordenamiento incorrecto.")
    if not search_attr in ["email", "dni", "name", "surname"]:
        return (False, "Atributo de busqueda incorrecto.")
    if start_profession and not start_profession in professions:
        return (False, "Profesión de busqueda incorrecta.")

    if page:
        try:
            int(page)
        except:
            return (False, "Tipo de página inválido.")
    
    return (True, "")

def check_show_data(
        types: List["DocumentType"],
        page: Optional[str],
        sort_attr: str,
        start_type: str) -> Tuple[bool, str]:
    if (page and not isinstance(page, str)) or not isinstance(sort_attr, str) or not isinstance(start_type, str):
        return (False, "Algúno de los tipos de los parámetros es incorrecto.")
    if not sort_attr in ["upload_date", "title"]:
        return (False, "Atributo de ordenamiento incorrecto.")
    if start_type and not start_type in types:
        return (False, "Tipo de documento de busqueda incorrecto.")
    
    if page:
        try:
            int(page)
        except:
            return (False, "Tipo de página inválido.")

    return (True, "")

def check_employee_data(employee_data) -> Tuple[bool, str]:
    if not employee_data["name"] or not employee_data["surname"] or not employee_data["dni"] or not employee_data["street"] or not employee_data["number"] or not employee_data["email"] or not employee_data["locality"] or not employee_data["phone"] or not employee_data["profession_id"] or not employee_data["job_position_id"] or not employee_data["emergency_contact_name"] or not employee_data["emergency_contact_phone"] or not employee_data["obra_social"] or not employee_data["affiliate_number"]:
        return (False, "Faltó rellenar campos obligatorios.")

    if len(employee_data["name"]) > 100:
        return (False, "El nombre debe ser menor a 100 caracteres.")
    if len(employee_data["surname"]) > 100:
        return (False, "El apellido debe ser menor a 100 caracteres.")
    if len(employee_data["dni"]) > 120 or not is_valid_dni(employee_data["dni"]):
        return (False, "Error en el dni ingresado.")
    if len(employee_data["street"]) > 255:
        return (False, "La calle debe ser menor a 255 caracteres.")
    if len(employee_data["number"]) > 10:
        return (False, "El número debe ser menor a 10 caracteres.")
    if employee_data["apartment"] and len(employee_data["apartment"]) > 10:
        return (False, "El departamento debe ser menor a 10 caracteres.")
    if len(employee_data["email"]) > 120 or not is_valid_email(employee_data["email"]) or not domain_exists(employee_data["email"]):
        return (False, "Error en el email ingresado.")
    if len(employee_data["phone"]) > 20 or not is_valid_phone(employee_data["phone"]):
        return (False, "Error en el telefono ingresado.")
    if len(employee_data["emergency_contact_name"]) > 100:
        return (False, "El nombre del contacto de emergencia debe ser menor a 100 caracteres.")
    if len(employee_data["emergency_contact_phone"]) > 20 or not is_valid_phone(employee_data["emergency_contact_phone"]):
        return (False, "Error en el telefono del contacto de emergencia.")
    if len(employee_data["obra_social"]) > 100:
        return (False, "La obra social debe ser menor a 100 caracteres.")
    if len(employee_data["affiliate_number"]) > 50:
        return (False, "El número de afiliado debe ser menor a 50 caracteres.")
    if employee_data["start_date"] and not is_valid_date(employee_data["start_date"]):
        return (False, "Fecha de inicio no válida.")
    if employee_data["end_date"] and not is_valid_date(employee_data["end_date"]):
        return (False, "Fecha de cese no válida.")

    try:
        locality_ids = [locality.id for locality in locality_operations.list_localitys()]
        if not int(employee_data["locality"]) in locality_ids:
            return (False, "ID de localidad inexistente.")
    except:
        return (False, "Error en la localidad ingresada.")

    try:
        profession_ids = [profession.id for profession in profession_operations.list_professions()]
        if not int(employee_data["profession_id"]) in profession_ids:
            return (False, "ID de profesión inexistente.")
    except:
        return (False, "Error en la profesión ingresada.")
    
    try:
        job_position_ids = [job_position.id for job_position in job_position_operations.list_job_positions()]
        if not int(employee_data["job_position_id"]) in job_position_ids:
            return (False, "ID del puesto laboral inexistente.")
    except:
        return (False, "Error en el puesto laboral ingresado.")

    return (True, "")