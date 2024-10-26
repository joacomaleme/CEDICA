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
from src.web.handlers.auth import is_authenticated
import dns.resolver
import re

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.get("/")
def login():
    return render_template("auth/login.html")

def validate_authenticate(email, password):
    '''
        Revisa si las credenciales del usuario son correctas, si no lo son retorna una string describiendo el error, si las credenciales son correctas, pero
        el usuario se haya desactivado, retorna una string describiendo el error. En caso contrario retorna None.
    '''
    user = user_operations.authenticate_user(email, password)
    
    if not user:
        return 'Credenciales incorrectas'
    if not user.enabled:
        return 'Su cuenta se haya suspendida en este momento'
    return None


@bp.post("/authenticate")
def authenticate():
    '''
        Recibe en un formulario un email y contraseña, revisa si cualifica para iniciar sesión, si falla informa el error y retorna al usuario al login,
        en caso contrario regisra la sesión, entrega una cookie al usuario para que pueda acceder a su sesión, informa el éxito, y redirige al "Home"
    '''
    params = request.form
    email = str(params.get("email"))
    password = str(params.get("password"))
    
    error = validate_authenticate(email, password)
    if error:
        flash(error, "error")
        return redirect(url_for("auth.login"))
    else:
        session["user"] = email
        flash('Sesión iniciada con éxito', 'success')
        return redirect(url_for("home"))

@bp.get("/logout")
def logout():
    '''
    Cierra la sesión actual del usuario, si haya una activa. Redirige al login.
    '''
    if is_authenticated(session):
        del session["user"]
        session.clear()
        flash("Sesión cerrada correctamente", "info")
    else:
        flash("No se hayó ninguna sesión activa", "error")
    
    return redirect(url_for("auth.login"))

@bp.get("/registrar")
@permission_required('user_new')
def register():
    '''
        Renderiza el template auth/register.html, enviando los parametros necesarios en el mismo.
    '''
    roles = role_operations.list_roles()
    roles = [role.name for role in roles]
    users = user_operations.list_users()
    mails = [user.email for user in users]
    aliases = [user.alias for user in users]
    return render_template("auth/register.html", roles=roles, mails=mails, aliases=aliases)

def is_valid_email(email:str):
    '''
    Valida que el email recibido por parametro (string) cumpla con un patrón típico de mail. True si se cumple, False si no.
    '''
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def password_is_valid(password:str):
    '''
    Valida que la contraseña tenga una longitud válida, y aunque sea un número o caracter especial. Retorna True si se cumplen los criterios, False en caso
    contrario.
    '''
    pattern = r'(?=.*[\d])|(?=.*[\W_])'
    return re.search(pattern, password) is not None and len(password) >= 7

def domain_exists(email:str):
    '''
    Valida que exista un servidor MX para la dirección de mail pasada por parametro. Retorna True si existe, false si no.
    '''
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return False


def validate_upload(mail, alias, password, role, enabled):
    '''
        Valida que no estén repetidos el mail o el alias, que la contraseña cumpla los criterios de la aplicación, que el mail cumpla formato de mail, y 
        exista un servidor MX para el tipo de mail declarado, que no se intente iniciar a un Administrador de Sistema suspendido, y que los valores de ninguna
        variable sean más grandes de lo que la BD puede guardar. En caso de cualquier discrepancia con lo esperado, retorna una string notificando el error, 
        caso contrario retorna None.
    '''

    user_mail = user_operations.get_user_by_email(mail)
    user_alias = user_operations.get_user_by_alias(alias)
    if user_mail or user_alias: #Revisa si ya el mail o alias ya están registrados, no pueden haber repetidos
        return "Lo lamentamos, ha habido un error inesperado"
    
    if not password_is_valid(password): #Revisa que la contraseña cumpla los requisitos
        return "La contraseña no cumple con los patrones solicitados"

    if (not is_valid_email(mail)) or (not domain_exists(mail)): #Revisa existencia de dominio del mail, y formato de escritura
        return "La dirección de mail ingresada no es válida"

    if role and role.name == "Administrador de Sistema" and not enabled: #Revisa consistencia de parametros (admins no se pueden bannear)
        return "No se puede suspender a un Administrador de Sistema"

    if len(mail) > 120 or len(password) > 128 or len(alias) > 50: #Revisa que no hayan parametros que puedan romper la BD
        return 'Parametro demasiado largo, respete los límites por favor'
    
    return None

@bp.post("/upload")
@permission_required('user_new')
def upload():
    '''
        Recibe todos los parametros necesarios para crear un usuario por formulario (mail, alias, contraseña, y role.name, todas en formato string), así como
        una checkbox de si el usuario debe iniciar suspendido o no. Llama a validate_upload para validar los datos, si hay errores los informa, sino informa
        el éxito de la operación, al agregar a el nuevo usuario a la BD. Finalmente, independientemente de la presencia o ausencia de errores, redirige a
        a auth.register.
    '''
    params = request.form

    mail = str(params.get("email"))
    alias = str(params.get("alias"))
    password = str(params.get("password"))
    role = role_operations.search_name(params.get("role"))
    enabled = params.get("enabled") is None

    error = validate_upload(mail, alias, password, role, enabled)
    if error:
        flash(error, "error")
        return redirect((url_for("auth.register")))

    if role:
        user_operations.create_user(mail, alias, password, role.id, enabled)
    else:
        user_operations.create_user(mail, alias, password, None, enabled)

    flash("Usuario registrado exitosamente", "success")
    return redirect((url_for("auth.register")))