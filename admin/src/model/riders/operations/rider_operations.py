from src.model.database import db
from src.model.riders.tables.rider import Rider
from sqlalchemy.orm  import Query
from typing import List, Optional


"""
    Funcion que toma todos los parametros necesarios para crear un Rider, lo instancia y lo agrega a la base de datos.
"""
def create_rider(
    name: str, last_name: str, dni: str, age: int, birth_date: str,
    birth_locality_id: int, birth_province_id: int, 
    address_street: str, address_number: str, address_apartment: Optional[str],
    current_locality_id: int, current_province_id: int, phone: str,
    emergency_contact_name: str, emergency_contact_phone: str, 
    has_scholarship: bool, scholarship_percentage: Optional[float],
    has_disability_certificate: bool, disability_diagnosis_id: Optional[int],
    disability_type_id: Optional[int], receives_family_allowance: bool,
    family_allowance_type_id: Optional[int], receives_pension: bool,
    pension_type_id: Optional[int], health_insurance: Optional[str], 
    affiliate_number: Optional[str], has_guardianship: bool, 
    school_id: Optional[int], current_grade: Optional[str],
    attending_professionals: Optional[str], institution_work_proposal: str, 
    active: str, institution_sede: str, work_days: Optional[str],
    teacher_id: Optional[int], horse_conductor_id: Optional[int], 
    horse_id: Optional[int], track_assistant_id: Optional[int]
) -> Rider:
    rider = Rider(
        name=name, last_name=last_name, dni=dni, age=age, birth_date=birth_date,
        birth_locality_id=birth_locality_id, birth_province_id=birth_province_id, 
        address_street=address_street, address_number=address_number, address_apartment=address_apartment,
        current_locality_id=current_locality_id, current_province_id=current_province_id, phone=phone,
        emergency_contact_name=emergency_contact_name, emergency_contact_phone=emergency_contact_phone, 
        has_scholarship=has_scholarship, scholarship_percentage=scholarship_percentage,
        has_disability_certificate=has_disability_certificate, disability_diagnosis_id=disability_diagnosis_id,
        disability_type_id=disability_type_id, receives_family_allowance=receives_family_allowance,
        family_allowance_type_id=family_allowance_type_id, receives_pension=receives_pension,
        pension_type_id=pension_type_id, health_insurance=health_insurance, 
        affiliate_number=affiliate_number, has_guardianship=has_guardianship, 
        school_id=school_id, current_grade=current_grade,
        attending_professionals=attending_professionals, institution_work_proposal=institution_work_proposal, 
        active=active, institution_sede=institution_sede, work_days=work_days,
        teacher_id=teacher_id, horse_conductor_id=horse_conductor_id, 
        horse_id=horse_id, track_assistant_id=track_assistant_id
    )
    db.session.add(rider)
    db.session.commit()
    db.session.expunge(rider)
    return rider

"""
    Lista a todos los jinetes, NO usar sin una necesidad clara.
"""
def list_riders():
    riders = Rider.query.all()
    [db.session.expunge(rider) for rider in riders]
    return riders


"""
    Devuelve un jinete con un id especifico
"""
def get_rider(id: int) -> Optional[Rider]:
    rider = Rider.query.get(id)
    if rider:
        db.session.expunge(rider)
    return rider

"""
    Devuelve un jinete con un dni especifico
"""
def get_rider_by_dni(dni: str) -> Optional[Rider]:
    rider = Rider.query.filter(Rider.dni == dni).first()
    if rider:
        db.session.expunge(rider)
    return rider


"""
    Actualiza un jinete dado otro objeto de tipo Rider
"""

def __update_rider__(to_update: Rider) -> Rider:
    rider = Rider.query.get(to_update.id)
    if rider is None:
        raise ValueError("No se encontró un jinete con ese ID")

    rider.name = to_update.name or rider.name
    rider.last_name = to_update.last_name or rider.last_name
    rider.dni = to_update.dni or rider.dni
    rider.age = to_update.age or rider.age
    rider.birth_date = to_update.birth_date or rider.birth_date
    rider.birth_locality_id = to_update.birth_locality_id or rider.birth_locality_id
    rider.birth_province_id = to_update.birth_province_id or rider.birth_province_id
    rider.address_street = to_update.address_street or rider.address_street
    rider.address_number = to_update.address_number or rider.address_number
    rider.address_apartment = to_update.address_apartment or rider.address_apartment
    rider.current_locality_id = to_update.current_locality_id or rider.current_locality_id
    rider.current_province_id = to_update.current_province_id or rider.current_province_id
    rider.phone = to_update.phone or rider.phone
    rider.emergency_contact_name = to_update.emergency_contact_name or rider.emergency_contact_name
    rider.emergency_contact_phone = to_update.emergency_contact_phone or rider.emergency_contact_phone
    rider.has_scholarship = to_update.has_scholarship if to_update.has_scholarship is not None else rider.has_scholarship
    rider.scholarship_percentage = to_update.scholarship_percentage if to_update.scholarship_percentage is not None else rider.scholarship_percentage
    rider.has_disability_certificate = to_update.has_disability_certificate if to_update.has_disability_certificate is not None else rider.has_disability_certificate
    rider.disability_diagnosis_id = to_update.disability_diagnosis_id or rider.disability_diagnosis_id
    rider.disability_type_id = to_update.disability_type_id or rider.disability_type_id
    rider.receives_family_allowance = to_update.receives_family_allowance if to_update.receives_family_allowance is not None else rider.receives_family_allowance
    rider.family_allowance_type_id = to_update.family_allowance_type_id or rider.family_allowance_type_id
    rider.receives_pension = to_update.receives_pension if to_update.receives_pension is not None else rider.receives_pension
    rider.pension_type_id = to_update.pension_type_id or rider.pension_type_id
    rider.health_insurance = to_update.health_insurance or rider.health_insurance
    rider.affiliate_number = to_update.affiliate_number or rider.affiliate_number
    rider.has_guardianship = to_update.has_guardianship if to_update.has_guardianship is not None else rider.has_guardianship
    rider.school_id = to_update.school_id or rider.school_id
    rider.current_grade = to_update.current_grade or rider.current_grade
    rider.attending_professionals = to_update.attending_professionals or rider.attending_professionals
    rider.institution_work_proposal = to_update.institution_work_proposal or rider.institution_work_proposal
    rider.active = to_update.active if to_update.active is not None else rider.active
    rider.institution_sede = to_update.institution_sede or rider.institution_sede
    rider.work_days = to_update.work_days or rider.work_days
    rider.teacher_id = to_update.teacher_id or rider.teacher_id
    rider.horse_conductor_id = to_update.horse_conductor_id or rider.horse_conductor_id
    rider.horse_id = to_update.horse_id or rider.horse_id
    rider.track_assistant_id = to_update.track_assistant_id or rider.track_assistant_id

    db.session.commit()
    db.session.expunge(rider)
    return rider


"""
    Elimina un jinete dado un id especifico
"""
def delete_rider(id: int):
    rider = Rider.query.get(id)
    if not rider:
        raise ValueError("No se encontró un jinete con ese ID")
    db.session.delete(rider)
    db.session.commit()


"""
    Cambia el estado de la flag "active" para un jinete especifico
"""
def toggle_active(id: int) -> Rider:
    rider = Rider.query.get(id)
    if not rider:
        raise ValueError("No se encontró un jinete con ese ID")
    rider.active = 'DE BAJA' if rider.active == 'REGULAR' else 'REGULAR'
    db.session.commit()
    db.session.expunge(rider)
    return rider



"""
    WIP
"""
