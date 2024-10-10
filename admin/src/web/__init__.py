from flask import Flask, render_template
from flask_session import Session
from src.model.encrypt import bcrypt
from src.web.handlers import error
from src.web.controllers.user_controller import bp as user_bp
from src.web.controllers.auth import bp as auth_bp
from src.web.handlers.auth import is_authenticated
from src.model import database
from src.model.config import config
from src.model import seeds

session = Session()

def create_app(env="development", static_folder="../../static"):
    
    #APP START
    app = Flask(__name__, static_folder=static_folder)    
    app.config.from_object(config[env])
    database.init_app(app)
    session.init_app(app)

    #ENCRIPTACIÓN
    bcrypt.init_app(app)
    
    #ROUTES, BLUEPRINTS, Y HANDLERS
    @app.route("/")
    def home():
        return render_template('home.html')
    #---
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    #---
    app.register_error_handler(404, error.error_not_found)
    app.register_error_handler(401, error.error_unauthorized)
    #---

    # Registro funciones en jinja
    app.jinja_env.globals.update(is_authenticated=is_authenticated)
    
    #COMANDOS:
    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command("seed-db")
    def seed_db():
        seeds.run()
        print("Base de datos sembrada")

    return app
