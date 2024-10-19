from flask import abort, redirect, render_template, request, url_for
from flask import Blueprint, flash, current_app
from src.model.generic.operations import document_types_operations
from src.web.handlers.check_permission import permission_required
from src.model.riders.operations import disability_diagnosis_operations
from src.model.riders.operations import disability_type_operations
from src.model.riders.operations import family_allowance_type_operations
from src.model.riders.operations import guardian_operations
from src.model.riders.operations import guardian_rider_operations
from src.model.riders.operations import pension_type_operations
from src.model.riders.operations import rider_operations
from src.model.riders.operations import school_operations
from src.model.riders.operations import work_day_operations
from src.model.generic.operations import locality_operations
from src.model.generic.operations import province_operations
from src.model.generic.operations import address_operations
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
        riders = rider_operations.list_riders()
        localitys = locality_operations.list_localitys()
        provinces = province_operations.list_provinces()
        documents = document_operations.list_documents_by__rider_id(rider.id)
        
        # document_types = document_types_operations.list_document_type()
        # start_document_type = request.args.get('start-document-type') or ""
        mode = request.args.get("mode", "general")

        documents = document_operations.list_documents_by__rider_id(rider.id)
        
        # document_types = document_types_operations.list_document_type()
        # start_document_type = request.args.get('start-document-type') or ""
        mode = request.args.get("mode", "general")

        # Traigo el address y locality por ser una copia
        address = address_operations.get_addres(rider.address_id)
        locality = locality_operations.get_locality(rider.locality_id)

        rider.address = address
        rider.locality = locality

        mails = [rider.email for rider in riders]
        dnis = [rider.dni for rider in riders]
        affiliate_numbers = [rider.affiliate_number for rider in riders]
       
        mails.remove(rider.email)
        dnis.remove(rider.dni)
        affiliate_numbers.remove(rider.affiliate_number)
        
        return render_template("riders/show.html", rider=rider, localitys=localitys, professions=professions, job_positions=job_positions,
                                documents=documents, mails=mails, dnis=dnis, affiliate_numbers=affiliate_numbers,
                                mode=mode)
    else:
        return abort(404)

def to_spanish(attr: str) -> str:
    match attr:
        case "name":
            return "nombre"
        case "last_name":
            return "apellido"
        case _:
            return attr