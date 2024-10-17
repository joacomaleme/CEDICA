from flask import abort, redirect, render_template, request, url_for
from flask import Blueprint, flash, current_app
from src.model.generic.operations import document_types_operations
from src.web.handlers.check_permission import permission_required
from src.model.riders.operations import disability_diagnosis_operations
from src.model.riders.operations import disability_type_operations
from src.model.riders.operations import family_allowance_type_operations
from src.model.riders.operations import guardian_operations
from src.model.riders.operations import guardian_rider_operations
from src.model.riders.operations import horse_operations
from src.model.riders.operations import pension_type_operations
from src.model.riders.operations import rider_operations
from src.model.riders.operations import school_operations
from src.model.riders.operations import sede_operations
from src.model.riders.operations import work_day_operations
from src.model.riders.operations import work_proposal_operations
from src.model.generic.operations import locality_operations
from src.model.generic.operations import province_operations
from uuid import uuid4

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

    return render_template("riders/index.html", pages=pages, riders=riders, localities=localities, provices=provinces, start_sort_attr=start_sort_attr,
                            start_search_attr=start_search_attr, search_attr_esp=search_attr_esp, start_search_val=start_search_val,
                            start_ascending=(not start_ascending), start_page=page)

@bp.route("/profile/<int:rider_id>")
def profile(rider_id):
    wanted_rider = rider_operations.get_rider(rider_id)
    return render_template("riders/view_rider.html", rider=wanted_rider)

def to_spanish(attr: str) -> str:
    match attr:
        case "name":
            return "nombre"
        case "surname":
            return "apellido"
        case _:
            return attr