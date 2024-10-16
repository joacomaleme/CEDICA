from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, inspect



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
        Funcion para reiniciar la base de datos. Hace uso del engine de SQLAlchemy para acceder a la base de datos y usando la funcion text (para enviar comandos SQLs como texto a la db) realizar las operaciones de DDL
    """

    print("Borrando Base de Datos...")
    # Recupero la database engine
    engine = db.engine
    # Recupero el inspector de la db
    inspector = inspect(engine)
    # Recupero todos los nombres de las tablas
    table_names = inspector.get_table_names()

    # Desabilito los checkeos de ForeignKeys
    with engine.connect() as conn:
        conn.execute(text('SET CONSTRAINTS ALL DEFERRED'))
        # Elimino todas las tablas
        for table in table_names:
            conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
        conn.commit()

    # Creo todas las tablas
    print("Creando Base de Datos...")
    db.create_all()

    # Habilito los checkeos de ForeignKeys
    with engine.connect() as conn:
        conn.execute(text('SET CONSTRAINTS ALL IMMEDIATE'))
        conn.commit()
    print("Base de Datos Creada.")
