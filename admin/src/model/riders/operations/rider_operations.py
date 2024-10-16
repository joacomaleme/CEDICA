from src.model.database import db
from src.model.riders.tables.rider import Rider
from sqlalchemy.orm  import Query
from typing import Optional
from datetime import date

"""
    Funcion que toma todos los parametros necesarios para crear un Rider, lo instancia y lo agrega a la base de datos.
"""


def create_rider(name: str, last_name: str, dni: str, age: int, birth_date: date,
                 birth_locality_id: int, birth_province_id: int, address_id: int,
                 current_locality_id: int, current_province_id: int, phone: str,
                 emergency_contact_name: str, emergency_contact_phone: str,
                 active: bool, sede: str, has_scholarship: bool = False, scholarship_percentage: Optional[float] = None,
                 has_disability_certificate: bool = False, disability_diagnosis_id: Optional[int] = None,
                 disability_type_id: Optional[int] = None, receives_family_allowance: bool = False,
                 family_allowance_type_id: Optional[int] = None, receives_pension: bool = False,
                 pension_type_id: Optional[int] = None, health_insurance: Optional[str] = None,
                 affiliate_number: Optional[str] = None, has_guardianship: bool = False,
                 school_id: Optional[int] = None, current_grade: Optional[str] = None,
                 attending_professionals: Optional[str] = None, work_proposal: Optional[str] = None,
                 teacher_id: Optional[int] = None, horse_conductor_id: Optional[int] = None,
                 horse_id: Optional[int] = None, track_assistant_id: Optional[int] = None,
                 is_indebt: bool = False, debt: float = 0.0) -> Rider:
    
    rider = Rider(
        name=name, last_name=last_name, dni=dni, age=age, birth_date=birth_date,
        birth_locality_id=birth_locality_id, birth_province_id=birth_province_id, address_id=address_id,
        current_locality_id=current_locality_id, current_province_id=current_province_id, phone=phone,
        emergency_contact_name=emergency_contact_name, emergency_contact_phone=emergency_contact_phone,
        active=active, sede=sede, has_scholarship=has_scholarship, scholarship_percentage=scholarship_percentage,
        has_disability_certificate=has_disability_certificate, disability_diagnosis_id=disability_diagnosis_id,
        disability_type_id=disability_type_id, receives_family_allowance=receives_family_allowance,
        family_allowance_type_id=family_allowance_type_id, receives_pension=receives_pension,
        pension_type_id=pension_type_id, health_insurance=health_insurance,
        affiliate_number=affiliate_number, has_guardianship=has_guardianship,
        school_id=school_id, current_grade=current_grade,
        attending_professionals=attending_professionals, work_proposal=work_proposal,
        teacher_id=teacher_id, horse_conductor_id=horse_conductor_id,
        horse_id=horse_id, track_assistant_id=track_assistant_id, is_indebt=is_indebt, debt=debt
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
    rider.address_id = to_update.address_id or rider.address_id
    rider.current_locality_id = to_update.current_locality_id or rider.current_locality_id
    rider.current_province_id = to_update.current_province_id or rider.current_province_id
    rider.phone = to_update.phone or rider.phone
    rider.emergency_contact_name = to_update.emergency_contact_name or rider.emergency_contact_name
    rider.emergency_contact_phone = to_update.emergency_contact_phone or rider.emergency_contact_phone
    rider.active = to_update.active if to_update.active is not None else rider.active
    rider.sede = to_update.sede or rider.sede
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
    rider.work_proposal = to_update.work_proposal or rider.work_proposal
    rider.teacher_id = to_update.teacher_id or rider.teacher_id
    rider.horse_conductor_id = to_update.horse_conductor_id or rider.horse_conductor_id
    rider.horse_id = to_update.horse_id or rider.horse_id
    rider.track_assistant_id = to_update.track_assistant_id or rider.track_assistant_id
    rider.is_indebt = to_update.is_indebt or rider.is_indebt
    rider.debt = to_update.debt or rider.debt

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
    rider.active = not rider.active
    db.session.commit()
    db.session.expunge(rider)
    return rider



"""
    Operaciones de busqueda especificas
"""


# Ordena por un atributo específico (nombre por defecto)
def sorted_by_attribute(riders: Query, attribute: str = "name", ascending: bool = True) -> Query:
    return riders.order_by(getattr(Rider, attribute).asc() if ascending else getattr(Rider, attribute).desc())

# Búsqueda por nombre
def search_by_name(riders: Query, name: str = "") -> Query:
    if name:
        return riders.filter(Rider.name.ilike(f"%{name}%"))
    return riders

# Búsqueda por apellido
def search_by_surname(riders: Query, surname: str = "") -> Query:
    if surname:
        return riders.filter(Rider.surname.ilike(f"%{surname}%"))
    return riders

# Búsqueda por DNI
def search_by_dni(riders: Query, dni: Optional[int] = None) -> Query:
    if dni is not None:
        return riders.filter(Rider.dni == dni)
    return riders

# Búsqueda por profesional
def search_by_professional(riders: Query, professional: str = "") -> Query:
    if professional:
        return riders.filter(Rider.professional.ilike(f"%{professional}%"))
    return riders

# Función final que combina los filtros y búsquedas
def get_riders_filtered_list(page: int,
                             limit: int = 25,
                             sort_attr: str = "name",
                             ascending: bool = True,
                             search_name: str = "",
                             search_surname: str = "",
                             search_dni: Optional[int] = None,
                             search_professional: str = "") -> Query:           ## Tener en cuenta que profesional que lo atiende es TEXT
    # Inicia la consulta con Rider
    riders = Rider.query
    
    # Aplica los filtros y búsquedas
    riders = search_by_name(riders, search_name)
    riders = search_by_surname(riders, search_surname)
    riders = search_by_dni(riders, search_dni)
    riders = search_by_professional(riders, search_professional)
    
    # Ordena los resultados
    riders = sorted_by_attribute(riders, sort_attr, ascending)
    
    # Pagina los resultados
    rider_list = riders.paginate(page=page, per_page=limit, error_out=False)
    
    # Expulsa los objetos de la sesión
    [db.session.expunge(rider) for rider in rider_list.items]
    
    return rider_list


