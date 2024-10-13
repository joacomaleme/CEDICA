from flask import redirect, render_template, request, url_for
from flask import Blueprint, flash, current_app
from src.web.handlers.check_permission import permission_required
from src.model.employees.operations import employee_operations
from src.model.employees.operations import job_position_operations
from src.model.employees.operations import profession_operations
from src.model.generic.operations import document_operations
from uuid import uuid4
import re

bp = Blueprint("employee", __name__, url_prefix="/empleados")

@bp.route("/")
# @permission_required('employee_index')
def index():
    professions = profession_operations.list_professions()
    professions = [profession.name for profession in professions]
    job_positions = job_position_operations.list_job_positions()
    job_positions = [job_position.name for job_position in job_positions]

    page = request.args.get('page')
    ascending = request.args.get('ascending') is None
    sort_attr = request.args.get('sort_attr') or "inserted_at"
    search_attr = request.args.get('search_attr') or "email"
    search_value = request.args.get('search_value') or ""

    start_sort_attr = ""
    start_search_attr = ""
    start_search_val = ""

    try:
        if not page:
            page = 1
        else:
            page = int(page)

        data = employee_operations.get_employees_filtered_list(page=page, sort_attr=sort_attr, ascending=ascending, search_attr=search_attr, search_value=search_value)

        employees = data[0]
        pages = data[1]
        
    except:
        flash("Uso inválido de parametros, no se pudo aplicar el filtro", "error")
        page = 0

    return render_template("employees/index.html", pages=pages, employees=employees, professions=professions, job_positions=job_positions,
                            start_sort_attr=start_sort_attr, start_search_attr=start_search_attr, start_search_val=start_search_val,
                            start_ascending=(not ascending), start_page=page)

# @bp.route("/")
# def index():
#     employees = employee_operations.list_employees()
#     return render_template("employees/index.html", employees=employees)

@bp.get("/nuevo")
@permission_required('employee_new')
def new():
    employees = employee_operations.list_employees()
    professions = profession_operations.list_professions()
    job_positions = job_position_operations.list_job_positions()

    mails = [employee.email for employee in employees]
    dnis = [employee.dni for employee in employees]
    affiliate_numbers = [employee.affiliate_number for employee in employees]

    return render_template("employees/new.html", professions=professions, job_positions=job_positions,
                           mails=mails, dnis=dnis, affiliate_numbers=affiliate_numbers)

@bp.post("/create")
@permission_required('employee_create')
def create():
    params = request.form

    employee_data = {
        "name": params.get("name"),
        "surname": params.get("surname"),
        "dni": params.get("dni"),
        "address": params.get("address"),
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

    employee = employee_operations.create_employee(**employee_data)

    if "files" in request.files:
        files = request.files.getlist("files")
        print(files)

        # Tomo el cliente
        client = current_app.storage.client

        for file in files:
            filename = remove_extension(file.filename)
            path = f"{uuid4()}-{file.filename}" # Uso uuid4() para generar un número random y que no se repita el nombre
            content_type = file.content_type

            document_operations.create_document(filename, content_type, path, employee_id=employee.id)

            # Tomo el tamaño del archivo
            file_content = file.read()
            size = len(file_content)
            file.seek(0)

            # Subo a MINIO
            client.put_object("grupo03", path, file.stream, size, content_type=content_type)

    return redirect(url_for("employee.index"))

@bp.put("/<int:id>/update")
@permission_required('employee_update')
def update(id):
    params = request.form
    print(params)

    return redirect(url_for("employee.index"))

@bp.delete("/<int:id>/delete")
@permission_required('employee_delete')
def delete(id):
    employee_operations.delete_employee(id)
    return redirect(url_for("employee.index"))

# Utils functions
def is_valid_email(email :str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def remove_extension(path: str) -> str:
    split = path.split(".")
    return ".".join(split[:-1]) if len(split) > 1 else path