from src.model.database import db
from src.model.riders.tables.horse import Horse

def create_horse(name, gender, breed, age, active):
    horse = Horse(name=name, gender=gender, breed=breed, age=age, active=active)
    db.session.add(horse)
    db.session.commit()
    db.session.expunge(horse)
    return horse

def get_horse(horse_id):
    horse = Horse.query.get(horse_id)
    db.session.expunge(horse)
    return horse

def delete_horse(horse_id):
    horse = Horse.query.get(horse_id)
    if horse is None:
        raise ValueError("No se encontro un caballo con ese ID")
    db.session.delete(horse)
    db.session.commit()
