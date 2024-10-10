from flask import render_template
from flask import Blueprint
from src.model.auth.operations import user_operations
from src.web.handlers.auth import is_authenticated
from flask import session
from flask import abort


bp = Blueprint("user", __name__, url_prefix="/usuarios")

@bp.route("/")
def index():
    if not is_authenticated(session):
        return abort(401)
    user = user_operations.list_users()
    return render_template("home.html", users = user)
