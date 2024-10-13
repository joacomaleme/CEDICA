from src.model.database import db
from src.model.generic.tables.locality import Locality

# Operaciones del CRUD para localidades

def create_locality(name):
    locality = Locality(name=name)
    db.session.add(locality)
    db.session.commit()
    db.session.expunge(locality)
    return locality

