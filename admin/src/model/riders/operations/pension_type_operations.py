from src.model.database import db
from src.model.riders.tables.pension_type import PensionType

def create_pension_type(name):
    pension_type = PensionType(name=name)
    db.session.add(pension_type)
    db.session.commit()
    db.session.expunge(pension_type)
    return pension_type

def get_pension_type(pension_type_id):
    pension_type = PensionType.query.get(pension_type_id)
    db.session.expunge(pension_type)
    return pension_type

def delete_pension_type(pension_type_id):
    pension_type = PensionType.query.get(pension_type_id)
    if pension_type is None:
        raise ValueError("No se encontro un tipo de pension con ese ID")
    db.session.delete(pension_type)
    db.session.commit()
