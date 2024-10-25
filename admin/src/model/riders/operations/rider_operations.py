from src.model.database import db
from src.model.riders.tables.rider import Rider
from sqlalchemy.orm  import Query
from typing import Optional
from datetime import date

def create_rider(name: str, last_name: str, dni: str, age: int, birth_date: date,
                 birth_locality_id: int, birth_province_id: int, address_id: int,
                 current_locality_id: int, current_province_id: int, phone: str,
                 emergency_contact_name: str, emergency_contact_phone: str,
                 active: bool, sede_id: str, has_scholarship: bool = False, scholarship_percentage: Optional[float] = None,
                 has_disability_certificate: bool = False, disability_diagnosis_id: Optional[int] = None,
                 disability_type_id: Optional[int] = None, receives_family_allowance: bool = False,
                 family_allowance_type_id: Optional[int] = None, receives_pension: bool = False,
                 pension_type_id: Optional[int] = None, health_insurance: Optional[str] = None,
                 affiliate_number: Optional[str] = None, has_guardianship: bool = False,
                 school_id: Optional[int] = None, current_grade: Optional[str] = None,
                 attending_professionals: Optional[str] = None, work_proposal_id: Optional[str] = None,
                 teacher_id: Optional[int] = None, horse_conductor_id: Optional[int] = None,
                 horse_id: Optional[int] = None, track_assistant_id: Optional[int] = None,
                 is_indebt: bool = False, debt: float = 0.0,
                 guardian1_name: Optional[str] = None, guardian1_last_name: Optional[str] = None, guardian1_dni: Optional[str] = None,
                 guardian1_address_id: Optional[int] = None, guardian1_locality_id: Optional[int] = None, guardian1_province_id: Optional[int] = None,
                 guardian1_phone: Optional[str] = None, guardian1_email: Optional[str] = None, guardian1_education_level: Optional[str] = None,
                 guardian1_occupation: Optional[str] = None, guardian1_relationship: Optional[str] = None,
                 guardian2_name: Optional[str] = None, guardian2_last_name: Optional[str] = None, guardian2_dni: Optional[str] = None,
                 guardian2_address_id: Optional[int] = None, guardian2_locality_id: Optional[int] = None, guardian2_province_id: Optional[int] = None,
                 guardian2_phone: Optional[str] = None, guardian2_email: Optional[str] = None, guardian2_education_level: Optional[str] = None,
                 guardian2_occupation: Optional[str] = None, guardian2_relationship: Optional[str] = None) -> Rider:
    
    rider = Rider(
        name=name, last_name=last_name, dni=dni, age=age, birth_date=birth_date,
        birth_locality_id=birth_locality_id, birth_province_id=birth_province_id, address_id=address_id,
        current_locality_id=current_locality_id, current_province_id=current_province_id, phone=phone,
        emergency_contact_name=emergency_contact_name, emergency_contact_phone=emergency_contact_phone,
        active=active, sede_id=sede_id, has_scholarship=has_scholarship, scholarship_percentage=scholarship_percentage,
        has_disability_certificate=has_disability_certificate, disability_diagnosis_id=disability_diagnosis_id,
        disability_type_id=disability_type_id, receives_family_allowance=receives_family_allowance,
        family_allowance_type_id=family_allowance_type_id, receives_pension=receives_pension,
        pension_type_id=pension_type_id, health_insurance=health_insurance,
        affiliate_number=affiliate_number, has_guardianship=has_guardianship,
        school_id=school_id, current_grade=current_grade,
        attending_professionals=attending_professionals, work_proposal_id=work_proposal_id,
        teacher_id=teacher_id, horse_conductor_id=horse_conductor_id,
        horse_id=horse_id, track_assistant_id=track_assistant_id, is_indebt=is_indebt, debt=debt,
        
        # Nuevos campos para los guardians
        guardian1_name=guardian1_name, guardian1_last_name=guardian1_last_name, guardian1_dni=guardian1_dni,
        guardian1_address_id=guardian1_address_id, guardian1_locality_id=guardian1_locality_id, guardian1_province_id=guardian1_province_id,
        guardian1_phone=guardian1_phone, guardian1_email=guardian1_email, guardian1_education_level=guardian1_education_level,
        guardian1_occupation=guardian1_occupation, guardian1_relationship=guardian1_relationship,
        guardian2_name=guardian2_name, guardian2_last_name=guardian2_last_name, guardian2_dni=guardian2_dni,
        guardian2_address_id=guardian2_address_id, guardian2_locality_id=guardian2_locality_id, guardian2_province_id=guardian2_province_id,
        guardian2_phone=guardian2_phone, guardian2_email=guardian2_email, guardian2_education_level=guardian2_education_level,
        guardian2_occupation=guardian2_occupation, guardian2_relationship=guardian2_relationship
    )
    db.session.add(rider)
    db.session.commit()
    db.session.expunge(rider)
    return rider

def list_riders():
    """
    Lista a todos los jinetes, NO usar sin una necesidad clara.
    """
    riders = Rider.query.all()
    [db.session.expunge(rider) for rider in riders]
    return riders

def get_rider(id: int) -> Optional[Rider]:
    """
    Devuelve un jinete con un id especifico
    """
    rider = Rider.query.get(id)
    if rider:
        db.session.expunge(rider)
    return rider

def get_rider_by_dni(dni: str) -> Optional[Rider]:
    """
    Devuelve un jinete con un dni especifico
    """
    rider = Rider.query.filter(Rider.dni == dni).first()
    if rider:
        db.session.expunge(rider)
    return rider

def get_rider_by_affiliate_number(affiliate_number: str) -> Optional[Rider]:
    rider = Rider.query.filter(Rider.affiliate_number == affiliate_number).first()
    if rider:
        db.session.expunge(rider)
    return rider


"""
    Actualiza un jinete dado otro objeto de tipo Rider
"""
def employee_exists(employee_id: int) -> bool:
    """
    Retorna True o False dependiendo si el empleado recibido está relacionado
    o no con algún jinete
    """
    rider = Rider.query.filter(db.or_(Rider.teacher_id==employee_id, Rider.horse_conductor_id==employee_id, Rider.track_assistant_id==employee_id)).first()
    return rider is not None

def __update_rider__(to_update: Rider) -> Rider:

    """
    Actualiza un jinete dado otro objeto de tipo Rider
    """
    rider = Rider.query.get(to_update.id)
    if rider is None:
        raise ValueError("No se encontró un jinete con ese ID")
    
    # Atributos existentes
    rider.name = to_update.name or rider.name
    rider.last_name = to_update.last_name or rider.last_name
    rider.dni = to_update.dni or rider.dni
    rider.age = to_update.age or rider.age
    rider.birth_date = to_update.birth_date or rider.birth_date
    rider.birth_locality_id = to_update.birth_locality_id or rider.birth_locality_id
    rider.birth_province_id = to_update.birth_province_id or rider.birth_province_id
    rider.address_id = to_update.address_id or rider.address_id
    rider.current_locality_id = to_update.current_locality_id or rider.current_locality_id
    rider.current_province_id = to_update.current_province_id or rider.current_province_id
    rider.phone = to_update.phone or rider.phone
    rider.emergency_contact_name = to_update.emergency_contact_name or rider.emergency_contact_name
    rider.emergency_contact_phone = to_update.emergency_contact_phone or rider.emergency_contact_phone
    rider.active = to_update.active if to_update.active is not None else rider.active
    rider.sede_id = to_update.sede_id or rider.sede_id
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
    rider.work_proposal_id = to_update.work_proposal_id or rider.work_proposal_id
    rider.teacher_id = to_update.teacher_id or rider.teacher_id
    rider.horse_conductor_id = to_update.horse_conductor_id or rider.horse_conductor_id
    rider.horse_id = to_update.horse_id or rider.horse_id
    rider.track_assistant_id = to_update.track_assistant_id or rider.track_assistant_id
    rider.is_indebt = to_update.is_indebt or rider.is_indebt
    rider.debt = to_update.debt or rider.debt

    # Nuevos atributos para los guardians
    rider.guardian1_name = to_update.guardian1_name or rider.guardian1_name
    rider.guardian1_last_name = to_update.guardian1_last_name or rider.guardian1_last_name
    rider.guardian1_dni = to_update.guardian1_dni or rider.guardian1_dni
    rider.guardian1_address_id = to_update.guardian1_address_id or rider.guardian1_address_id
    rider.guardian1_locality_id = to_update.guardian1_locality_id or rider.guardian1_locality_id
    rider.guardian1_province_id = to_update.guardian1_province_id or rider.guardian1_province_id
    rider.guardian1_phone = to_update.guardian1_phone or rider.guardian1_phone
    rider.guardian1_email = to_update.guardian1_email or rider.guardian1_email
    rider.guardian1_education_level = to_update.guardian1_education_level or rider.guardian1_education_level
    rider.guardian1_occupation = to_update.guardian1_occupation or rider.guardian1_occupation
    rider.guardian1_relationship = to_update.guardian1_relationship or rider.guardian1_relationship

    rider.guardian2_name = to_update.guardian2_name or rider.guardian2_name
    rider.guardian2_last_name = to_update.guardian2_last_name or rider.guardian2_last_name
    rider.guardian2_dni = to_update.guardian2_dni or rider.guardian2_dni
    rider.guardian2_address_id = to_update.guardian2_address_id or rider.guardian2_address_id
    rider.guardian2_locality_id = to_update.guardian2_locality_id or rider.guardian2_locality_id
    rider.guardian2_province_id = to_update.guardian2_province_id or rider.guardian2_province_id
    rider.guardian2_phone = to_update.guardian2_phone or rider.guardian2_phone
    rider.guardian2_email = to_update.guardian2_email or rider.guardian2_email
    rider.guardian2_education_level = to_update.guardian2_education_level or rider.guardian2_education_level
    rider.guardian2_occupation = to_update.guardian2_occupation or rider.guardian2_occupation
    rider.guardian2_relationship = to_update.guardian2_relationship or rider.guardian2_relationship

    db.session.commit()
    db.session.expunge(rider)
    return rider

def delete_rider(id: int):
    """
    Elimina un jinete dado un id especifico
    """
    rider = Rider.query.get(id)
    if not rider:
        raise ValueError("No se encontró un jinete con ese ID")
    db.session.delete(rider)
    db.session.commit()

def toggle_active(id: int) -> Rider:
    """
    Cambia el estado de la flag "active" para un jinete especifico
    """
    rider = Rider.query.get(id)
    if not rider:
        raise ValueError("No se encontró un jinete con ese ID")
    rider.active = not rider.active
    db.session.commit()
    db.session.expunge(rider)
    return rider

 # Operaciones de busqueda especificas #

# Ordena por un atributo específico (nombre por defecto)
def sorted_by_attribute(riders: Query, attribute: str = "name", ascending: bool = True) -> Query:
    return riders.order_by(getattr(Rider, attribute).asc() if ascending else getattr(Rider, attribute).desc())

def search_by_attribute(riders: Query, search_attr: str = "name", search_value: str = "") -> Query:
    match search_attr:
        case "name":
            return riders.filter(Rider.name.ilike(f"%{search_value}%"))
        case "last_name":
            return riders.filter(Rider.last_name.ilike(f"%{search_value}%"))
        case "dni":
            return riders.filter(Rider.dni.ilike(f"%{search_value}%"))
        case "professionals":
            return riders.filter(Rider.attending_professionals.ilike(f"%{search_value}%"))
        case _:
            return riders.filter(Rider.name.ilike(f"%{search_value}%"))

# Función final que combina los filtros y búsquedas
def get_riders_filtered_list(page: int,
                                limit: int = 25,
                                sort_attr: str = "name",
                                ascending: bool = True,
                                search_attr: str = "name",
                                search_value: str = "") -> Query:
    # Inicia la consulta con Rider
    riders = Rider.query
    
    # Aplica los filtros y búsquedas
    riders = search_by_attribute(riders, search_attr, search_value)
    
    # Ordena los resultados
    riders = sorted_by_attribute(riders, sort_attr, ascending)
    
    # Pagina los resultados
    rider_list = riders.paginate(page=page, per_page=limit, error_out=False)
    
    # Expulsa los objetos de la sesión
    [db.session.expunge(rider) for rider in rider_list.items]

    return (rider_list, ((riders.count()-1)//limit)+1)


