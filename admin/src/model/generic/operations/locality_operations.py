from src.model.database import db
from src.model.generic.tables.locality import Locality

# Operaciones del CRUD para localidades

def create_locality(name):
    locality = Locality(name=name)
    db.session.add(locality)
    db.session.commit()
    db.session.expunge(locality)
    return locality

def list_localitys():
    localitys = Locality.query.all()
    [db.session.expunge(locality) for locality in localitys]
    return localitys # puede devolver una lista vacia

def get_locality(id: int):
    locality = Locality.query.get(id)
    if locality:
        db.session.expunge(locality)
    return locality # si no encuentra nada devuelve None

def get_locality_by_name(name: str):
    locality = Locality.query.filter(Locality.name == name).first()
    if locality:
        db.session.expunge(locality)
    return locality # si no encuentra nada devuelve None