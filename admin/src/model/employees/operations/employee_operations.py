from datetime import datetime
from src.model.database import db
from src.model.employees.tables.employee import Employee
from src.model.employees.operations.profession_operations import search_name
from src.model.employees.operations.job_position_operations import search_name as job_search
from sqlalchemy.orm import Query
from typing import Optional, Tuple

def create_employee(name: str, surname: str, dni: str, address_id: int, email: str, locality_id: int, phone: str, profession_id: int, job_position_id: int, 
                    emergency_contact_name: str, emergency_contact_phone: str, obra_social: str, affiliate_number: str, is_volunteer: bool,
                    user_id: Optional[int] = None, enabled: bool = True, start_date: datetime = datetime.now(), end_date: Optional[datetime] = None) -> Employee:
    employee = Employee(name, surname, dni, address_id, email, locality_id, phone, profession_id, job_position_id, emergency_contact_name,
                        emergency_contact_phone, obra_social, affiliate_number, is_volunteer, enabled, user_id, start_date, end_date)
    db.session.add(employee)
    db.session.commit()
    db.session.expunge(employee)
    return employee

def list_employees():   # lista TODOS los employees (solo usar cuando sea estrictamente necesario)
    employees = Employee.query.all()
    [db.session.expunge(employee) for employee in employees]
    return employees # puede devolver una lista vacia

def list_employees_for_horses():   # lista TODOS los employees (solo usar cuando sea estrictamente necesario)
    domador = job_search("Domador")
    cuidador = job_search("Cuidador de Caballos")
    employees = Employee.query.filter(db.or_(Employee.job_position_id == domador.id, Employee.job_position_id == cuidador.id))

    [db.session.expunge(employee) for employee in employees]
    return employees # puede devolver una lista vacia

def get_employee(id: int):      #devuelve un employee dado un id
    employee = Employee.query.get(id)
    if employee:
        db.session.expunge(employee)
    return employee # si no encuentra nada devuelve None

def get_employee_by_dni(dni: str):
    employee = Employee.query.filter(Employee.dni == dni).first()
    if employee:
        db.session.expunge(employee)
    return employee # si no encuentra nada devuelve None

def get_employee_by_affiliate_number(affiliate_number: str):
    employee = Employee.query.filter(Employee.affiliate_number == affiliate_number).first()
    if employee:
        db.session.expunge(employee)
    return employee # si no encuentra nada devuelve None

def get_employee_by_email(email: str):      #devuelve un employee dado un email (el email es unico)
    employee = Employee.query.filter(Employee.email == email).first()
    if employee:
        db.session.expunge(employee)
    return employee # si no encuentra nada devuelve None

def update_employee(to_update: Employee) -> Employee:
    employee = Employee.query.get(to_update.id)
    if employee is None:
        raise ValueError("No se encontro un empleado con ese ID")

    employee.name = to_update.name or employee.name
    employee.surname = to_update.surname or employee.surname
    employee.dni = to_update.dni or employee.dni
    employee.address_id = to_update.address_id or employee.address_id
    employee.email= to_update.email or employee.email
    employee.locality_id = to_update.locality_id or employee.locality_id
    employee.phone = to_update.phone or employee.phone
    employee.profession_id = to_update.profession_id or employee.profession_id
    employee.job_position_id = to_update.job_position_id or employee.job_position_id
    employee.emergency_contact_name = to_update.emergency_contact_name or employee.emergency_contact_name
    employee.emergency_contact_phone = to_update.emergency_contact_phone or employee.emergency_contact_phone
    employee.obra_social = to_update.obra_social or employee.obra_social
    employee.affiliate_number = to_update.affiliate_number or employee.affiliate_number
    employee.start_date = to_update.start_date or employee.start_date
    employee.end_date = to_update.end_date or employee.end_date
    employee.is_volunteer = to_update.is_volunteer if to_update.is_volunteer is not None else employee.is_volunteer
    employee.enabled = to_update.enabled if to_update.enabled is not None else employee.enabled
    db.session.commit()
    db.session.expunge(employee)
    return employee

def delete_employee(id: int):
    employee = Employee.query.get(id)
    if employee is None:
        raise ValueError("No se encontro un emplead con ese ID")
    db.session.delete(employee)
    db.session.commit()

###INSTRUCCIONES DE UPDATE ESPECÍFICAS

def toggle_block(id: int) -> Employee:      # cambiar el estado de "enabled"
    employee = Employee.query.get(id)
    if employee is None:
        raise ValueError("No se encontro un empleado con ese ID") 
    employee.enabled = not employee.enabled
    db.session.commit()
    db.session.expunge(employee)
    return employee

def toggle_is_volunteer(id: int) -> Employee:       # cambiar el estado de "is_volunteer"
    employee = Employee.query.get(id)
    if employee is None:
        raise ValueError("No se encontro un empleado con ese ID")
    employee.is_volunteer = not employee.is_volunteer
    db.session.commit()
    db.session.expunge(employee)
    return employee

###INSTRUCCIONES DE LISTADO ESPECÍFICAS

# Ordena por un atributo específico (email por defecto)
def sorted_by_attribute(employees: Query, attribute: str = "inserted_at", ascending: bool = True) -> Query:
    return employees.order_by(getattr(Employee, attribute).asc() if ascending else getattr(Employee, attribute).desc())

def search_by_attribute(employees: Query, search_attr: str = "email", search_value: str = "") -> Query:
    match search_attr:
        case "email":
            return employees.filter(Employee.email.ilike(f"%{search_value}%"))
        case "name":
            return employees.filter(Employee.name.ilike(f"%{search_value}%"))
        case "surname":
            return employees.filter(Employee.surname.ilike(f"%{search_value}%"))
        case "dni":
            return employees.filter(Employee.dni.ilike(f"%{search_value}%"))
        case _:
            return employees.filter(Employee.email.ilike(f"%{search_value}%"))

def filter_profession(employees: Query, profession_name: str) -> Query:
    profession = search_name(profession_name)
    if profession:
        return employees.filter(db.and_(Employee.profession_id.isnot(None), Employee.profession_id == profession.id))
    else:
        return employees

# Función final que combina los filtros y búsquedas
def get_employees_filtered_list(page: int,
                                limit: int = 25,
                                sort_attr: str = "email",
                                ascending: bool = True,
                                search_attr: str = "email",
                                search_value: str = "",
                                search_profession: str = "") -> Tuple[Employee, int]:
    # Inicia la consulta con Employee
    employees = Employee.query
    
    # Aplica los filtros y búsquedas
    employees = search_by_attribute(employees, search_attr, search_value)
    employees = filter_profession(employees, search_profession)
    
    # Ordena los resultados
    employees = sorted_by_attribute(employees, sort_attr, ascending)
    
    # Pagina los resultados
    employee_list = employees.paginate(page=page, per_page=limit, error_out=False)
    
    # Expulsa los objetos de la sesión
    [db.session.expunge(employee) for employee in employee_list.items]

    return (employee_list, ((employees.count()-1)//limit)+1)
