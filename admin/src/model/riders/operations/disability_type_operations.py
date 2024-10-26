from src.model.database import db
from src.model.riders.tables.disability_type import DisabilityType

def create_disability_type(type):
    disability_type = DisabilityType(type=type)
    db.session.add(disability_type)
    db.session.commit()
    db.session.expunge(disability_type)
    return disability_type

def list_disability_type():
    disabilities_type = DisabilityType.query.all()
    [db.session.expunge(disability_type) for disability_type in disabilities_type]
    return disabilities_type

def get_disability_type(disability_type_id):
    disability_type = DisabilityType.query.get(disability_type_id)
    db.session.expunge(disability_type)
    return disability_type

def delete_disability_type(disability_type_id):
    disability_type = DisabilityType.query.get(disability_type_id)
    if disability_type is None:
        raise ValueError("No se encontro un tipo de discapacidad con ese ID")
    db.session.delete(disability_type)
    db.session.commit()
