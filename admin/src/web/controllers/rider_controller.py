from flask import render_template
from flask import Blueprint
from src.model.riders.operations import rider_operations

bp = Blueprint("rider", __name__, url_prefix="/JyA")

@bp.route("/")
def index():
    riders_list = rider_operations.list_riders()
    return render_template("listadoJyA.html", riders = riders_list)

@bp.route("/profile/<int:rider_id>")
def profile(rider_id):
    wanted_rider = rider_operations.get_rider(rider_id)
    return render_template("riderProfile.html", rider=wanted_rider)
