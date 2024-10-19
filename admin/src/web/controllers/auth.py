from flask import Blueprint
from flask import render_template
from flask import request
from flask import url_for
from flask import session
from flask import redirect
from flask import flash
from src.model.auth.operations import user_operations
from src.model.auth.operations import role_operations
from src.web.handlers.check_permissions import permission_required
import dns.resolver
import re

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.get("/")
def login():
    return render_template("auth/login.html")

@bp.post("/authenticate")
def authenticate():
    params = request.form
    user = user_operations.authenticate_user(str(params.get("email")), str(params.get("password")))
    
    if not user:
        flash('Credenciales incorrectas', 'error')
        return redirect(url_for("auth.login"))
    if not user.enabled:
        flash('Su cuenta se haya suspendida en este momento', 'error')
        return redirect(url_for("auth.login"))

    session["user"] = user.email
    flash('Sesión iniciada con éxito', 'success')
    return redirect(url_for("home"))

@bp.get("/logout")
def logout():
    if session.get("user"):
        del session["user"]
        session.clear()
        flash("Sesión cerrada correctamente", "info")
    else:
        ("No se hayó ninguna sesión activa", "error")
    
    return redirect(url_for("auth.login"))

@bp.get("/registrar")
@permission_required('user_new')
def register():
    roles = role_operations.list_roles()
    roles = [role.name for role in roles]
    users = user_operations.list_users()
    mails = [user.email for user in users]
    aliases = [user.alias for user in users]
    return render_template("auth/register.html", roles=roles, mails=mails, aliases=aliases)

def is_valid_email(email:str):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def password_is_valid(password:str):
    pattern = r'(?=.*[\d])|(?=.*[\W_])'
    return re.search(pattern, password) is not None and len(password) >= 7

def domain_exists(email:str):
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return False

@bp.post("/upload")
@permission_required('user_new')
def upload():
    params = request.form

    mail = str(params.get("email"))
    password = str(params.get("password"))
    checkMail = user_operations.get_user_by_email(mail)
    checkAlias = user_operations.get_user_by_alias(str(params.get("alias")))
    enabled = params.get("enabled") is None

    if checkMail or checkAlias:
        flash("Lo lamentamos, ha habido un error inesperado", "error")
        return redirect((url_for("auth.register")))
    if not password_is_valid(password):
        flash("La contraseña no cumple con los patrones solicitados", "error")
        return redirect((url_for("auth.register")))
    if (not is_valid_email(mail)) or (not domain_exists(mail)):
        flash("La dirección de mail ingresada no es válida", "error")
        return redirect((url_for("auth.register")))
    if params["role"] == "Administrador de Sistema":
        enabled = True

    if len(mail) > 1024 or len(password) > 128 or len(str(params.get("alias"))) > 50:
        flash('Parametro demasiado largo', "error")
        return redirect((url_for("auth.register")))

    role = role_operations.search_name(params["role"])
    user_operations.create_user(mail, params.get("alias"), password, role, enabled)
    flash("Usuario registrado exitosamente", "success")
    return redirect((url_for("auth.register")))