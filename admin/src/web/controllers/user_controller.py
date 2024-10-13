from flask import render_template
from flask import Blueprint
from src.model.auth.operations import user_operations
from src.model.auth.operations import role_operations
from src.web.handlers.check_login import login_required
from flask import session
from flask import abort
from flask import flash
from flask import request


bp = Blueprint("user", __name__, url_prefix="/usuarios")

@bp.route("/")
@login_required()
def index():
    roles = role_operations.list_roles()
    roles = [role.name for role in roles]

    mail = request.args.get('mail')
    page = request.args.get('page')
    role = request.args.get('role')
    ascending = request.args.get('ascending') is None
    users = user_operations.start_query()
    retMail=""
    retRole=""
    orderMail = request.args.get('order_email') is not None
    try:
        if not page:
            page = 1
        else:
            page = int(page)
        if mail:
            users = user_operations.search_by_mail(users, str(mail))
            retMail=mail
        if role:
            users = user_operations.filter_role(users, str(role))
            retRole=role
        if not orderMail:
            users = user_operations.sorted_by_attribute(users=users, attribute="email", ascending=ascending)
        else:
            users = user_operations.sorted_by_attribute(users, "inserted_at", ascending)
        if request.args.get('status'):
            users = user_operations.filter_active(users, bool(int(request.args.get('value'))))
    except:
        flash("Uso inválido de parametros, no se pudo aplicar el filtro", "error")
        page = 0
    finally:
        data = user_operations.get_paginated_list(users, page, 2)
        users = data[0]
        pages = data[1]
        return render_template("user_search.html", pages=pages, users=users, roles=roles, status=request.args.get('status'), startMail=retMail, startRole=retRole, startAscending=(not ascending), enabled=request.args.get('value'), orderMail=orderMail, startPage=page)
