from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy(session_options={'expire_on_commit': False})


def init_app(app):
    """
    Inicializa la base de datos con la aplicacion de Flask.
    """

    db.init_app(app)
    config(app)

    return app


def config(app):
    """
    Configuracion de hooks para la base de datos
    """

    @app.teardown_appcontext
    def close_session(exception=None):
        db.session.close()
    return app


def reset():
    """
    Resetea la base de datos.
    """
    print("Eliminando base de datos...")
    db.session.execute(text('DROP TABLE IF EXISTS users CASCADE;'))
    db.session.commit()
    db.drop_all()  # Drop other tables
    print("Creando base nuevamente...")
    db.create_all()
    print("Done!")
