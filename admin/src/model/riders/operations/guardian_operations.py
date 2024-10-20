from src.model.database import db
from src.model.riders.tables.guardian import Guardian
from src.model.riders.tables.rider_guardian import RiderGuardian

def create_guardian(name: str, last_name: str, dni: int, address_id: int, locality_id: int, province_id: int, phone: str, email: str, education_level: str, occupation: str):
    guardian = Guardian(name=name, last_name=last_name, dni=dni, address_id=address_id, locality_id=locality_id, province_id=province_id, phone=phone, email=email, education_level=education_level, occupation=occupation)
    db.session.add(guardian)
    db.session.commit()
    db.session.expunge(guardian)
    return guardian

def list_guardians():
    guardians = Guardian.query.all()
    [db.session.expunge(guardian) for guardian in guardians]
    return guardians

def get_guardians_by_rider_id(rider_id: int):
    guardians = (
        db.session.query(Guardian)
        .join(RiderGuardian)
        .filter(RiderGuardian.rider_id == rider_id)
        .all()
    )
    [db.session.expunge(guardian) for guardian in guardians]
    return guardians

def get_guardian(guardian_id):
    guardian = Guardian.query.get(guardian_id)
    db.session.expunge(guardian)
    return guardian

def delete_guardian(guardian_id):
    guardian = Guardian.query.get(guardian_id)
    if guardian is None:
        raise ValueError("No se encontro un guardian con ese ID")
    db.session.delete(guardian)
    db.session.commit()

    def __init__(self, name: str, last_name: str, dni: int, address_id: int, locality_id: int, province_id: int, phone: str, email: str, education_level: str, occupation: str):
        self.name = name
        self.last_name = last_name
        self.dni = dni
        self.address_id = address_id
        self.locality_id = locality_id
        self.province_id = province_id
        self.phone = phone
        self.email = email
        self.education_level = education_level
        self.occupation = occupation
