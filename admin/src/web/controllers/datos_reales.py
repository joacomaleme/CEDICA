from flask import render_template
from flask import Blueprint

bp = Blueprint("datos_reales", __name__, url_prefix="/dataSecreta")

@bp.get("/")
def index():
    datos = board.list_datos_reales()

    return render_template("datos_reales/index.html", datos_reales = datos)
