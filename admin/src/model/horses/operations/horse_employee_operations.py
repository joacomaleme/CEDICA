from src.model.database import db
from src.model.horses.tables.horse_employee import HorseEmployee

def create_horse_employee(horse_id: int, employee_id: int) -> HorseEmployee:
    horse_employee = HorseEmployee(horse_id, employee_id)
    db.session.add(horse_employee)
    db.session.commit()
    db.session.expunge(horse_employee)
    return horse_employee

def list_horse_employee_by_horse_id(horse_id: int):
    horses_employees = HorseEmployee.query.filter(HorseEmployee.horse_id == horse_id)
    if horses_employees is None:
        raise ValueError("No se encontro una relacion entre Caballo y Empleado con ese ID  de empleado")

    [db.session.expunge(horse_employee) for horse_employee in horses_employees]
    return horses_employees

def delete_horse_employee(horse_id, employee_id: int):
    horse_employee = HorseEmployee.query.filter(db.and_(HorseEmployee.horse_id == horse_id, HorseEmployee.employee_id == employee_id)).first()
    if horse_employee is None:
        raise ValueError("No se encontro ninguna relacion entre Caballo y Empleado con esos ID")

    db.session.delete(horse_employee)
    db.session.commit()