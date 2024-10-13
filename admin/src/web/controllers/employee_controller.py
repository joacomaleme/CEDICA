from flask import redirect, render_template, request, url_for
from flask import Blueprint, flash
from src.model.employees.operations import employee_operations
from src.model.employees.operations import job_position_operations
from src.model.employees.operations import profession_operations
import re

bp = Blueprint("employee", __name__, url_prefix="/empleados")

@bp.route("/")
def index():
    employees = employee_operations.list_employees()
    return render_template("employees/index.html", employees=employees)

@bp.get("/nuevo")
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

    employee_operations.create_employee(**employee_data)

    return redirect(url_for("employee.index"))

@bp.put("/<int:id>/update")
def update(id):
    params = request.form
    print(params)

    return redirect(url_for("employee.index"))


@bp.delete("/<int:id>/delete")
def delete(id):
    employee_operations.delete_employee(id)
    return redirect(url_for("employee.index"))

def is_valid_email(email:str):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
