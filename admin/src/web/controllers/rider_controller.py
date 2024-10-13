from flask import render_template
from flask import Blueprint
#from src.model.auth.operations import riders_operations Esto aún no está codeado


bp = Blueprint("rider", __name__, url_prefix="/JyA")

BD = [
        {'id': 1, 'name': 'Ivy Daguerre', 'role': 'ADC'},
        {'id': 2, 'name': 'Joaco Malchanki', 'role': 'TOP'},
        {'id': 3, 'name': 'Ingeniero Chavez', 'role': 'Ingeniero'}
]

@bp.route("/")
def index():
    #riders_list = riders_operations.list_riders()
    riders_list = BD
    return render_template("listadoJyA.html", riders = riders_list)

@bp.route("/profile/<int:rider_id>")
def profile(rider_id):
    #wanted_rider = riders_operations.get_rider(rider_id)
    wanted_rider = next((rider for rider in BD if rider['id'] == rider_id), None)
    
    if wanted_rider is None:
        abort(404)
    
    return render_template("riderProfile.html", rider=wanted_rider)
