from flask import redirect, render_template, request, url_for
from flask import Blueprint
from src.model.employees.operations import employee_operations
from src.model.employees.operations import job_position_operations
from src.model.employees.operations import profession_operations

bp = Blueprint("employee", __name__, url_prefix="/empleados")

@bp.route("/")
def index():
    employees = employee_operations.list_employees()
    return render_template("employees/index.html", employees=employees)

@bp.get("/nuevo")
def new():
    professions = profession_operations.list_professions()
    job_positions = job_position_operations.list_job_positions()
    return render_template("employees/new.html", professions=professions, job_positions=job_positions)

@bp.post("/create")
def create():
    params = request.form

    print(params.get("volunteer"), params.get("enabled"))

    # Convert form data to correct types
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
        "is_volunteer": params.get("volunteer") == 'on',  # Convert to bool
        "enabled": params.get("enabled") == 'on',  # Convert to bool
        "start_date": params.get("start-date"),
        "end_date": params.get("end-date"),
    }

    print(employee_data)

    # Call your employee creation method, unpacking the dictionary
    employee_operations.create_employee(**employee_data)

    return redirect(url_for("employee.index"))

@bp.put("/<int:id>/update")
def update(id):
    params = request.form
    print(params)

    return redirect(url_for("employees.index"))