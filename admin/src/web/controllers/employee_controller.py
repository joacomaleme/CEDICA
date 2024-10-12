from flask import redirect, render_template, request, url_for
from flask import Blueprint
from src.model.employees.operations import employee_operations


bp = Blueprint("employee", __name__, url_prefix="/empleados")

@bp.route("/")
def index():
    employees = employee_operations.list_employees()
    return render_template("employees/index.html", employees=employees)

@bp.get("/new")
def new():
    return render_template("employees/new.html")

@bp.post("/create")
def create():
    params = request.form
    print(params)

    return redirect(url_for("employees.index"))

@bp.put("/<int:id>/update")
def update(id):
    params = request.form
    print(params)

    return redirect(url_for("employees.index"))