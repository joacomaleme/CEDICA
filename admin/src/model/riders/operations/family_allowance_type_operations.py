from src.model.database import db
from src.model.riders.tables.family_allowance_type import FamilyAllowanceType

def create_family_allowance_type(name):
    family_allowance_type = FamilyAllowanceType(name=name)
    db.session.add(family_allowance_type)
    db.session.commit()
    db.session.expunge(family_allowance_type)
    return family_allowance_type

def get_family_allowance_type(family_allowance_type_id):
    family_allowance_type = FamilyAllowanceType.query.get(family_allowance_type_id)
    db.session.expunge(family_allowance_type)
    return family_allowance_type

def delete_family_allowance_type(family_allowance_type_id):
    family_allowance_type = FamilyAllowanceType.query.get(family_allowance_type_id)
    if family_allowance_type is None:
        raise ValueError("No se encontro una Family Allowance con ese ID")
    db.session.delete(family_allowance_type)
    db.session.commit()
