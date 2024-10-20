from src.model.database import db
from src.model.generic.tables.sede import Sede

def create_sede(name):
    sede = Sede(name=name)
    db.session.add(sede)
    db.session.commit()
    db.session.expunge(sede)
    return sede

def list_sedes():
    sedes = Sede.query.all()
    [db.session.expunge(sede) for sede in sedes]
    return sedes


def get_sede(sede_id):
    sede = Sede.query.get(sede_id)
    db.session.expunge(sede)
    return sede

def delete_sede(sede_id):
    sede = Sede.query.get(sede_id)
    if sede is None:
        raise ValueError("No se encontro una sede con ese ID")
    db.session.delete(sede)
    db.session.commit()
