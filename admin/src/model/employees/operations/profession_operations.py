from src.model.database import db
from src.model.employees.tables.profession import Profession

def create_profession(name: str) -> Profession:
    profession = Profession(name)
    db.session.add(profession)
    db.session.commit()
    db.session.expunge(profession)
    return profession

def list_professions():
    professions = Profession.query.all()
    [db.session.expunge(profession) for profession in professions]
    return professions