from flask import Blueprint

bp = Blueprint("auth", __name__, url_prefix="/auth")

bp.get("")
def login():
    return render_template("auth/login.html")

bp.post("/authenticate")
def authenticate():
    pass

bp.get("/logout")
def logout():
    pass