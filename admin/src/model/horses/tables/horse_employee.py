from src.model.database import db

"""
    Relación entre Horses y Employee (pueden haber muchos miembros del equipo asignados a un mismo caballo y viceversa)
"""

class HorseEmployee(db.Model):
    __tablename__ = 'horses_employees'
    id = db.Column(db.BigInteger, primary_key=True)  # Identificador único
    horse_id = db.Column(db.BigInteger, db.ForeignKey('horses.id', ondelete="CASCADE"))
    employee_id = db.Column(db.BigInteger, db.ForeignKey('employees.id', ondelete="CASCADE"))

    __table_args__ = (
        db.UniqueConstraint('horse_id', 'employee_id', name='_horse_employee_uc'),  # Ensures unique combination of rider and guardian
    )

    def __init__(self, horse_id, employee_id):
        self.horse_id = horse_id
        self.employee_id = employee_id
