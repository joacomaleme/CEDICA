from src.model.database import db
from src.model.riders.tables.school import School
from typing import Optional

def create_school(name: str, address: str, phone: str, observations: Optional[str] = None) -> School:
    school = School(name=name, address=address, phone=phone, observations=observations)
    db.session.add(school)
    db.session.commit()
    db.session.expunge(school)
    return school

def list_schools():
    schools = School.query.all()
    [db.session.expunge(school) for school in schools]
    return schools

def get_school(school_id):
    school = School.query.get(school_id)
    db.session.expunge(school)
    return school

def delete_school(school_id):
    school = School.query.get(school_id)
    if school is None:
        raise ValueError("No se encontro una escuela con ese ID")
    db.session.delete(school)
    db.session.commit()
