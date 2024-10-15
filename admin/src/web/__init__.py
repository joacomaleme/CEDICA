from flask import Flask, render_template
from src.web.storage import storage
from src.web.handlers import error
from src.web.controllers.user_controller import bp as user_bp
from src.web.controllers.employee_controller import bp as employee_bp
from src.web.handlers.auth import is_authenticated, is_permitted, is_self
from src.model import database
from src.model.config import config
from src.model import seeds

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
    
    # cargo la informacion y registro la bd
    app.config.from_object(config[env])
    database.init_app(app)
    
    # registro el object storage
    storage.init_app(app)


    @app.route("/")
    def home():
        return render_template('home.html')
    
    app.register_blueprint(user_bp)
    app.register_blueprint(employee_bp)

    app.register_error_handler(404, error.error_not_found)
    app.register_error_handler(401, error.error_unauthorized)
    app.register_error_handler(403, error.error_forbidden)
    #---

    # Registro funciones en jinja
    app.jinja_env.globals.update(is_authenticated=is_authenticated)
    app.jinja_env.globals.update(is_permitted=is_permitted)
    app.jinja_env.globals.update(is_self=is_self)

    
    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command("seed-db")
    def seed_db():
        seeds.run()
        print("Base de datos sembrada")

    return app
