from src.model.database import db
from src.model.board.user import User

def list_datos_reales():
    datos_reales = [
        {
            "numero_de_persona":1,
            "cantidad_de_horas_dormidas": "seis",
            "veces_que_se_comio_una_porcion_de_pizza_sin_respirar": "j@yahoo.web",
            "status": "de vez en cuando",
        },
        {
            "numero_de_persona":2,
            "cantidad_de_horas_dormidas": "papel",
            "veces_que_se_comio_una_porcion_de_pizza_sin_respirar": "yahoo@j.ñam",
            "status": "solo los viernes",
        },
    ]
    return datos_reales

def list_users():
    users = User.query.all()

    return users

def create_user(**kwargs):
    user = User(**kwargs)
    db.session.add(issue)
    db.session.commit()

    return user
