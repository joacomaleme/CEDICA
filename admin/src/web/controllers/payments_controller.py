from flask import Blueprint, render_template, request, abort, redirect, url_for, flash
from src.model.registers.operations import payment_operations, payment_type_operations
from src.web.handlers.check_permissions import permission_required
from src.model.employees.operations import employee_operations
from datetime import datetime

bp = Blueprint("payments", __name__, url_prefix="/pagos")

@bp.get("/")
@permission_required('payment_index')
def index():
    ascending = bool(request.args.get('ascending'))

    dfrom = request.args.get('from')
    until = request.args.get('until')

    if dfrom:
        try:
            dfrom = datetime.strptime(dfrom, '%Y-%m-%d')
        except:
            dfrom = datetime.strptime('1970-10-10', '%Y-%m-%d')
    else:
        dfrom = datetime.strptime('1970-10-10', '%Y-%m-%d')

    if until:
        try:
            until = datetime.strptime(until, '%Y-%m-%d')
        except:
            until = datetime.strptime('2100-10-10', '%Y-%m-%d')
    else:
        until = datetime.strptime('2100-10-10', '%Y-%m-%d')


    paym_name = request.args.get('type')
    role = []
    if paym_name:
        paym_name = str(paym_name)
        role = [payment_type_operations.get_payment_type_by_name(paym_name)]

    page = request.args.get('page')

    try:
        page = int(page)
    except:
        page = 1

    types = [p.name for p in payment_type_operations.list_payment_types()]
    payments = payment_operations.get_filtered_list(page, payment_types=role, ascending=ascending, start_date=dfrom, end_date=until)
    payment_types = [payment_type_operations.get_payment_type(pay.payment_type_id) for pay in payments[0]]

    if role:
        role = role[0].name
    else:
        role = ""
    return render_template("payments/index.html", until=until.strftime('%Y-%m-%d'), dfrom=dfrom.strftime('%Y-%m-%d'), startPage=page, pages=payments[1], payments=payments[0], payment_types=payment_types, startAscending=ascending, startType=role, types=types)


@bp.get("/registro/<id>")
@permission_required('payment_show')
def view_payment(id):
    payment = None
    try:
        payment = payment_operations.get_payment(int(id))
    except:
        payment = None
    if payment:
        return render_template("payments/view.html", payment=payment, emp=employee_operations.get_employee(payment.beneficiary_id), type=payment_type_operations.get_payment_type(payment.payment_type_id))
    else:
        return abort(404)
    
@bp.get("/registrar")
@permission_required('payment_create')
def register():
    types = payment_type_operations.list_payment_types()
    employees = employee_operations.list_employees()
    return render_template("payments/register.html", types=types, employees=employees)

@bp.post("/upload")
@permission_required('payment_create')
def upload():
    params = request.form
    monto = params.get('amount')
    date = params.get('date')
    pay_type = params.get('type')
    benef = params.get('emp')
    desc = params.get('desc')

    try:
        monto = float(monto)
    except:
        flash("Monto invalido", "error")
        return redirect(url_for("payments.register"))
    
    try:
        date = datetime.strptime(date, '%Y-%m-%d')
    except:
        flash("Fecha invalida", "error")
        return redirect(url_for("payments.register"))

    pay_type = payment_type_operations.get_payment_type_by_name(str(pay_type))
    if not pay_type:
        flash("Tipo de pago invalido", "error")
        return redirect(url_for("payments.register"))

    if pay_type.name == 'Honorarios':
        try:
            benef = int(benef)
            benef = employee_operations.get_employee(benef)
            if not benef:
                raise ValueError
            else:
                benef = benef.id
        except:
            flash('Pagos de honorarios requieren un empleado', "error")
            return redirect(url_for("payments.register"))
    else:
        benef = None

    if len(str(desc)) > 1024:
        flash('Descripción demasiado larga', "error")
        return redirect(url_for("payments.register"))

    payment_operations.create_payment(monto, date, str(desc), pay_type.id, benef)
    return redirect(url_for("payments.register"))