from flask import Blueprint, render_template, request, abort, redirect, url_for, flash
from src.model.registers.operations import collection_operations, collection_medium_operations
from src.model.registers.tables.collection import Collection
from src.web.handlers.check_permissions import permission_required
from src.model.employees.operations import employee_operations
from src.model.riders.operations import rider_operations
from datetime import datetime

bp = Blueprint("collection", __name__, url_prefix="/cobros")

@bp.get("/")
@permission_required('collection_index')
def index():
    ascending = bool(request.args.get('ascending'))

    dfrom = request.args.get('from')
    until = request.args.get('until')
    search_attr = request.args.get('search_attr') or "name"
    search_value = request.args.get('search_value') or ""

    start_search_attr = search_attr if search_attr else ""
    start_search_val = search_value if search_value else ""
    search_attr_esp = to_spanish(start_search_attr)

    if dfrom:
        try:
            dfrom = datetime.strptime(dfrom, '%Y-%m-%d').strftime('%Y-%m-%d')
        except:
            dfrom = ""
    else:
        dfrom = ""

    if until:
        try:
            until = datetime.strptime(until, '%Y-%m-%d').strftime('%Y-%m-%d')
        except:
            until = datetime.now().strftime('%Y-%m-%d')
    else:
      until = datetime.now().strftime('%Y-%m-%d')


    medium_name = request.args.get('medium')
    medium = []
    if medium_name:
        medium_name = str(medium_name)
        medium = [collection_medium_operations.get_collection_medium_by_name(medium_name)]

    page = request.args.get('page')

    if page:
        page = int(page)
    else:
        page = 1

    mediums = collection_medium_operations.list_collection_mediums()
    collections = collection_operations.get_filtered_list(page=page, collection_mediums=medium, ascending=ascending, start_date=dfrom,
                                                          end_date=until, search_attr=start_search_attr, search_value=start_search_val)
    collection_mediums = []

    for coll in collections[0]:
        for m in mediums:
            if coll.medium_id == m.id:
                collection_mediums.append(m)
                break

        coll.paid_by = rider_operations.get_rider(coll.paid_by_id)
        coll.received_by = employee_operations.get_employee(coll.received_by_id)

    if medium:
        medium = medium[0].name
    else:
        medium = ""

    return render_template("collections/index.html", until=until, dfrom=dfrom, startPage=page, pages=collections[1], collections=collections[0],
                            collection_mediums=collection_mediums, startAscending=ascending, start_medium=medium, start_search_attr=start_search_attr,
                            start_search_val=start_search_val, search_attr_esp=search_attr_esp, mediums=mediums)

@bp.get("/<id>")
@permission_required('collection_show')
def show(id):
    collection = collection_operations.get_collection(int(id))
    mediums = collection_medium_operations.list_collection_mediums()
    employees = employee_operations.list_employees()
    riders = rider_operations.list_riders()

    if collection:
        return render_template("collections/show.html", collection=collection, mediums=mediums, employees=employees, riders=riders)
    else:
        return abort(404)
    
@bp.get("/registrar")
@permission_required('collection_create')
def register():
    mediums = collection_medium_operations.list_collection_mediums()
    employees = employee_operations.list_employees()
    riders = rider_operations.list_riders()
    return render_template("collections/new.html", mediums=mediums, employees=employees, riders=riders)

@bp.post("/upload")
@permission_required('collection_create')
def upload():
    params = request.form
    monto = params.get('amount')
    date = params.get('date')
    medium = params.get('medium')
    received_by = params.get('emp')
    paid_by = params.get('rider')
    obs = params.get('obs')

    try:
        monto = float(monto)
    except:
        flash("Monto invalido", "error")
        return redirect(url_for("collection.register"))
    
    try:
        date = datetime.strptime(date, '%Y-%m-%d')
    except:
        flash("Fecha invalida", "error")
        return redirect(url_for("collection.register"))

    medium = collection_medium_operations.get_collection_medium(int(medium))
    if not medium:
        flash("Tipo de pago invalido", "error")
        return redirect(url_for("collection.register"))

    try:
        received_by = employee_operations.get_employee(int(received_by))
        if not received_by:
            raise ValueError
        else:
            received_by = received_by.id
    except:
        flash('Pagos de honorarios requieren un empleado', "error")
        return redirect(url_for("collection.register"))

    try:
        paid_by = rider_operations.get_rider(int(paid_by))
        if not paid_by:
            raise ValueError
        else:
            paid_by = paid_by.id
    except:
        flash('Pagos de honorarios requieren un empleado', "error")
        return redirect(url_for("collection.register"))


    if len(str(obs)) > 1024:
        flash('Descripción demasiado larga', "error")
        return redirect(url_for("collection.register"))

    collection_operations.create_collection(amount=monto, date=date, observations=str(obs), medium_id=medium.id,
                                            received_by_id=received_by, paid_by_id=paid_by)
    return redirect(url_for("collection.register"))

@bp.post("/<int:id>/update")
@permission_required('collection_update')
def update(id):
    real_id = int(id)
    params = request.form
    employees = employee_operations.list_employees()

    amount = params.get("amount")
    date = params.get("date")
    obs = params.get("obs")
    medium_id = params.get("medium")
    received_by_id = params.get("emp")
    paid_by_id = params.get("rider")
        
    try:
        collection = collection_operations.get_collection(real_id)

        if not collection:
            flash("Lo lamentamos, ha habido un error inesperado", "error")
            return redirect((url_for("home")))

        collection = Collection(amount=amount, date=date, observations=obs, medium_id=medium_id, received_by_id=received_by_id, paid_by_id=paid_by_id)
        collection.id = real_id
        collection_operations.update_collection(collection)

        return redirect(url_for("collection.show", id=collection.id))
    except:
        flash("Uso inválido de parametros, no se pudo actualizar el cobro", "error")
        return redirect(url_for("home"))

@bp.get("/<int:id>/delete")
@permission_required('collection_destroy')
def delete(id):
    collection_operations.delete_collection(id)
    return redirect(url_for("collection.index"))

def to_spanish(attr: str) -> str:
    match attr:
        case "name":
            return "nombre"
        case "surname":
            return "apellido"
        case _:
            return attr