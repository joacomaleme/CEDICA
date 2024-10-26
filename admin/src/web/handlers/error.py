from dataclasses import dataclass
from flask import render_template

@dataclass
class Error:
    code: int
    message: str
    description: str

def error_not_found(e):
    error = Error(404, "Página no encontrada", "Lo lamentamos, no hemos podido encontrar la URL solicitada, revise que esté correctamente escrita.")
    return render_template("error.html", error=error), 404

def error_unauthorized(e):
    error = Error(401, "No autenticado", "Usted es un usuario no autenticado, inicie sesión con sus credenciales antes de intentar acceder.")
    return render_template("error.html", error=error), 401

def error_forbidden(e):
    error = Error(403, "Prohibido", "No posee las credenciales adecuadas para acceder a esta página")
    return render_template("error.html", error=error), 403
