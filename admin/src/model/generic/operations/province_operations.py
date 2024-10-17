from src.model.database import db
from src.model.generic.tables.province import Province

# Operaciones del CRUD para provincias

def create_province(name):
    province = Province(name=name)
    db.session.add(province)
    db.session.commit()
    db.session.expunge(province)
    return province

def list_provinces():
    provinces = Province.query.all()
    [db.session.expunge(province) for province in provinces]
    return provinces # puede devolver una lista vacia

def get_province(id: int):
    province = Province.query.get(id)
    if province:
        db.session.expunge(province)
    return province # si no encuentra nada devuelve None