from flask import abort, redirect, render_template, request, url_for
from flask import Blueprint, flash
from src.web.handlers.check_permission import permission_required
from src.model.employees.operations import employee_operations
from src.model.generic.operations import document_operations
from src.model.generic.operations import document_types_operations
from src.model.generic.operations import sede_operations
from src.model.generic.operations import work_proposal_operations
from src.model.horses.tables.horse import Horse
from src.model.horses.operations import horse_operations
from src.model.horses.operations import horse_employee_operations
from datetime import datetime


bp = Blueprint("horse", __name__, url_prefix="/ecuestre")

@bp.route("/")
@permission_required('horse_index')
def index():
    activities = work_proposal_operations.list_work_proposals()
    activities = [activity.name for activity in activities]

    page = request.args.get('page')
    start_ascending = request.args.get('ascending') is None
    sort_attr = request.args.get('sort_attr') or "inserted_at"
    search_attr = "name"
    search_value = request.args.get('search_value') or ""

    start_activity = request.args.get('activity') or ""
    start_sort_attr = sort_attr if sort_attr else ""
    start_search_attr = search_attr if search_attr else ""
    start_search_val = search_value if search_value else ""
    search_attr_esp = to_spanish(start_search_attr)
    pages = 1
    horses = []

    try:
        try:
            page = int(page)
        except:
            page = 1

        try:
            if sort_attr not in ["inserted_at", "name", "birth"]:
                raise TypeError("Search attribute incorrecto")
            if start_sort_attr not in ["inserted_at", "name", "birth"]:
                raise TypeError("Search attribute incorrecto")
        except TypeError:
            sort_attr = start_sort_attr = "inserted_at"


        data = horse_operations.get_horses_filtered_list(page=page, sort_attr=sort_attr, ascending=start_ascending, search_attr=search_attr,
                                                         search_value=search_value, activity=start_activity)

        horses = data[0]
        pages = data[1]
    except Exception as e:
        print(e)
        flash("Uso inválido de parametros, no se pudo aplicar el filtro", "error")
        page = 0


    return render_template("horses/index.html", pages=pages, horses=horses, activities=activities, start_sort_attr=start_sort_attr, start_search_attr=start_search_attr, search_attr_esp=search_attr_esp, start_search_val=start_search_val, start_ascending=(not start_ascending), start_activity=start_activity, start_page=page)


@bp.get("/nuevo")
@permission_required('horse_create')
def new():
    activities = work_proposal_operations.list_work_proposals()
    sedes = sede_operations.list_sedes()
    employees = employee_operations.list_employees_for_horses()

    return render_template("horses/new.html", activities=activities, sedes=sedes, employees=employees)


@bp.post("/create")
@permission_required('horse_create')
def create():
    params = request.form

    horse_data = {
        "name": params.get("name"),
        "birth": params.get("birth"),
        "sex": params.get("sex") == "True",
        "breed": params.get("breed"),
        "coat": params.get("coat"),
        "is_donated": params.get("is-donated") == "True",
        "sede_id": params.get("sede"),
        "activity_id": params.get("activity"),
    }

    employees = params.getlist('employees')     # Se hace aparte porque son una tabla aparte
    employees = [int(employee) for employee in employees]

    try:
        if not check_data(horse_data):
            raise Exception
        if not check_employees(employees):
            raise Exception

        new_horse = horse_operations.create_horse(
            name = horse_data["name"],
            birth = horse_data["birth"],
            sex = horse_data["sex"],
            breed = horse_data["breed"],
            coat = horse_data["coat"],
            is_donated = horse_data["is_donated"],
            sede_id = horse_data["sede_id"],
            active = True,
            activity_id = horse_data["activity_id"],
        )
        for employee_id in employees:
            horse_employee_operations.create_horse_employee(horse_id=new_horse.id , employee_id=employee_id)
    except:
        flash("Uso inválido de parametros, no se pudo crear el caballo", "error")
        return redirect(url_for("home"))

    return redirect(url_for("horse.index"))


@bp.get("/<int:id>")
@permission_required('horse_show')
def show(id):
    horse = horse_operations.get_horse(id)

    if horse:
        sedes = sede_operations.list_sedes()
        activities = work_proposal_operations.list_work_proposals()
        employees = employee_operations.list_employees_for_horses()
        types = document_types_operations.list_document_type()
        documents = document_operations.list_documents_by_horse_id(id)

        existing_employees = horse_employee_operations.list_horse_employee_by_horse_id(id)
        existing_employees = [existing_employee.employee_id for existing_employee in existing_employees]

        page = request.args.get('page')
        start_ascending = request.args.get('ascending') is None
        sort_attr = request.args.get('sort_attr') or "upload_date"
        search_title = request.args.get('search_title') or ""
        start_type = request.args.get('type') or ""
        mode = request.args.get("mode", "general")
        pages = 1

        page = 1 if not page else int(page)

        # Traigo la sede por ser una copia
        sede = sede_operations.get_sede(horse.sede_id)

        data = document_operations.get_documents_filtered_list(documents=documents, page=page, sort_attr=sort_attr, ascending=start_ascending, search_title=search_title,
                                                                    search_type=start_type)
        horse.sede = sede
        documents = data[0]
        pages = data[1]

        return render_template("horses/show.html", horse=horse, sedes=sedes, activities=activities, types=types, documents=documents,
                               mode=mode, employees=employees, existing_employees=existing_employees, start_ascending=(not start_ascending),
                               sort_attr=sort_attr, search_title=search_title, start_type=start_type, pages=pages, startPage=page)
    else:
        return abort(404)


@bp.post("/<int:id>/update")
@permission_required('horse_update')
def update(id):
    try:
        real_id = int(id)
    except:
        flash("Uso inválido de parametros, caballo no existente", "error")
        return redirect(url_for("horse.index"))



    params = request.form   # Solicitud de los datos

    # guardado de empleados en variables y checkeo de su validez
    existing_employees = params.getlist("existing_employees")
    check_employees(existing_employees)
    employees = params.getlist("employees")
    check_employees(employees)


    horse_data = {
        "name": params.get("name"),
        "birth": params.get("birth"),
        "sex": params.get("sex") == 'True',
        "breed": params.get("breed"),
        "coat": params.get("coat"),
        "is_donated": params.get("is_donated") == "True",
        "sede_id": params.get("sede"),
        "active": params.get("active") == "on",
        "activity_id": params.get("activity"),
    }
    check_data(horse_data)


    try:
        horse = horse_operations.get_horse(real_id)

        if not horse:
            flash("Lo lamentamos, ha habido un error inesperado", "error")
            return redirect((url_for("home")))
        
        horse = Horse(
            name = horse_data["name"],
            birth = horse_data["birth"],
            sex = horse_data["sex"],
            breed = horse_data["breed"],
            coat = horse_data["coat"],
            is_donated = horse_data["is_donated"],
            sede_id = horse_data["sede_id"],
            active = horse_data["active"],
            activity_id = horse_data["activity_id"]
        )
        horse.id = real_id
        horse_operations.update_horse(horse)

        # Se actualizan las relaciones de empleados con el caballo editado
        for employee in employees:
            if employee not in existing_employees:
                horse_employee_operations.create_horse_employee(id, int(employee))
        for existing_employee in existing_employees:
            if existing_employee not in employees:
                horse_employee_operations.delete_horse_employee(id, int(existing_employee))


        return redirect(url_for("horse.show", id=horse.id))
    except:
        flash("Uso inválido de parametros, no se pudo actualizar el caballo", "error")
        return redirect(url_for("home"))


@bp.get("/<int:id>/delete")
@permission_required('horse_destroy')
def delete(id):
    try:
        real_id = int(id)
    except:
        flash("Uso inválido de parametros, caballo no existente", "error")
        return redirect(url_for("horse.index"))

    try:
        horse_operations.delete_horse(real_id)
        return redirect(url_for("horse.index"))
    except ValueError:
        flash("Uso inválido de parametros, no se pudo Borrar el caballo", "error")
        return redirect(url_for("home"))


# Utils function, pasa algunas palabras al espa;ol
def to_spanish(attr: str) -> str:
    match attr:
        case "name":
            return "nombre"
        case "breed":
            return "raza"
        case "coat":
            return "pelaje"
        case _:
            return attr


def check_data(horse_data) -> bool:
    # Verifica que el nombre no exceda los 100 caracteres
    if len(horse_data["name"]) > 100:
        return False
    # Verifica que la fecha de nacimiento sea válida
    if not is_valid_date(horse_data["birth"]):
       return False
    # Verifica que la raza no exceda los 100 caracteres
    if len(horse_data["breed"]) > 100:
        return False
    # Verifica que el pelaje no exceda los 64 caracteres
    if len(horse_data["coat"]) > 64:
        return False
    try:
        # Verifica que el 'sede_id' exista en la base de datos
        sede_ids = [sede.id for sede in sede_operations.list_sedes()]
        if not int(horse_data["sede_id"]) in sede_ids:
            return False
        # Verifica que el 'activity_id' exista en la base de datos
        activity_ids = [activity.id for activity in work_proposal_operations.list_work_proposals()]
        if not int(horse_data["activity_id"]) in activity_ids:
            return False
    except:
        return False

    # Si todas las verificaciones son correctas, retorna True
    return True


def check_employees(employees) -> bool:
    # Obtiene la lista de empleados válidos de la base de datos
    bd_employees = employee_operations.list_employees()
    valid_employee_ids = [employee.id for employee in bd_employees]
    # Verifica que cada empleado en la lista proporcionada esté en la lista de empleados válidos
    for employee in employees:
        if int(employee) not in valid_employee_ids:
            return False

    # Si todos los empleados son válidos, retorna True
    return True


def is_valid_date(date_str: str) -> bool:
    try:
        # Intenta convertir la cadena de fecha en un objeto datetime con el formato 'YYYY-MM-DD'
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        # Si ocurre un error de conversión, la fecha no es válida
        return False
