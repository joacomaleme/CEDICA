from flask import abort, redirect, render_template, request, url_for
from flask import Blueprint, flash, current_app
from src.model.generic.operations import document_operations
from src.model.generic.operations import document_types_operations
from src.web.handlers.check_permission import permission_required
from src.model.riders.operations import disability_diagnosis_operations
from src.model.riders.operations import disability_type_operations
from src.model.riders.operations import family_allowance_type_operations
from src.model.riders.operations import guardian_operations
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

        data = rider_operations.get_riders_filtered_list(page=page, limit=2, sort_attr=sort_attr, ascending=start_ascending, search_attr=search_attr,
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
        guardians = guardian_operations.get_guardians_by_rider_id(id)
        sedes = sede_operations.list_sedes()
        horses = horse_operations.list_horses()
        employees = employee_operations.list_employees()
        #Aca estaría bueno crear varias listas según el rol para que en la selección se ofrezcan los que trabajan de eso, pero no queda muy claro en las jobs positions
        
        document_types = document_types_operations.list_document_type()
        start_document_type = request.args.get('start-document-type') or ""

        rider.address = address_operations.get_addres(rider.address_id)
        school = schools[rider.school_id - 1]
        
        mode = request.args.get("mode", "general")
        
        dnis = [rider.dni for rider in riders]
        affiliate_numbers = [rider.affiliate_number for rider in riders]
        dnis.remove(rider.dni)
        affiliate_numbers.remove(rider.affiliate_number)

        return render_template("riders/show.html", rider=rider, localitys=localitys, provinces=provinces, disability_diagnosis=disability_diagnosis, disability_types = disability_types, family_allowance_types=family_allowance_types, pension_types=pension_types, schools=schools, work_proposals=work_proposals, work_days=work_days, guardians=guardians, sedes=sedes, horses=horses, employees=employees, school=school, dnis=dnis, affiliate_numbers=affiliate_numbers, documents=documents, mode=mode)
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
        "locality": params.get("locality"),
        "active": params.get("active") != None,
    }
 
    try:
        rider = rider_operations.get_rider(real_id)

        if not rider:
            flash("Lo lamentamos, ha habido un error inesperado", "error")
            return redirect((url_for("home")))
        #if (not is_valid_email(rider_data["email"])):
            #flash("La dirección de mail ingresada no es válida", "error")
            #return redirect((url_for("rider.show", id=rider.id)))

        #mails = [rider.email for rider in riders]
        dnis = [rider.dni for rider in riders]
        
        #mails.remove(rider.email)
        dnis.remove(rider.dni)

        if rider.dni in dnis:
            flash("La dirección de mail ingresada no es válida", "error")
            return redirect((url_for("rider.show", id=rider.id)))

        # Actualizo el address
        #address = Address(rider_data["street"], rider_data["number"], rider_data["apartment"])
        #address.id = rider.address_id
        #address_operations.update_address(address)

        rider = Rider(
            name = rider_data["name"],
            last_name = rider_data["surname"],
            dni = rider_data["dni"],
            current_locality_id = rider_data["locality"],
            active = rider_data["active"]
        )
        rider.id = real_id
        rider_operations.update_rider(rider)

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