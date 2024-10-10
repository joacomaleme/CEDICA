from flask import Blueprint
from flask import render_template
from flask import request
from flask import url_for
from flask import session
from flask import redirect
from flask import flash
from src.model.auth.operations import user_operations

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.get("/")
def login():
    return render_template("auth/login.html")

@bp.post("/authenticate")
def authenticate():
    params = request.form

    user = user_operations.authenticate_user(params["email"], str(params["password"]))
    
    if not user:
        flash('Credenciales incorrectas', 'error')
        return redirect(url_for("auth.login"))
    if not user.enabled:
        flash('Su cuenta se haya suspendida en este momento', 'error')
        return redirect(url_for("auth.login"))

    session["user"] = user.email
    flash('Sesión iniciada con éxito', 'success')
    return redirect(url_for("user.index"))

@bp.get("/logout")
def logout():
    if session.get("user"):
        del session["user"]
        session.clear()
        flash("Sesión cerrada correctamente", "info")
    else:
        ("No se hayó ninguna sesión activa", "error")
    
    return redirect(url_for("auth.login"))