from datetime import datetime
from src.model.database import db
from src.model.horses.tables.horse_employee import HorseEmployee
from src.model.employees.tables.job_position import JobPosition  # Ensure this is imported
from src.model.employees.tables.profession import Profession  # Ensure this is imported
from src.model.employees.tables.employee_document import EmployeeDocument
from typing import Optional

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(120), unique=True, nullable=False)
    address_id = db.Column(db.BigInteger, db.ForeignKey('addresses.id'), nullable=False)
    address = db.relationship('Address', foreign_keys=[address_id])
    email = db.Column(db.String(120), unique=True, nullable=False)
    locality_id = db.Column(db.BigInteger, db.ForeignKey('localities.id'), nullable=False)
    locality = db.relationship('Locality', foreign_keys=[locality_id])
    phone = db.Column(db.String(20), nullable=False)
    
    # Relación con Profession
    profession_id = db.Column(db.BigInteger, db.ForeignKey('professions.id'), nullable=False)
    profession = db.relationship('Profession', back_populates='employees')

    # Relación con JobPosition
    job_position_id = db.Column(db.BigInteger, db.ForeignKey('job_positions.id'), nullable=False)

    start_date = db.Column(db.Date, nullable=False, default=datetime.now())
    end_date = db.Column(db.Date, default=None)

    emergency_contact_name = db.Column(db.String(100), nullable=False)
    emergency_contact_phone = db.Column(db.String(20), nullable=False)

    obra_social = db.Column(db.String(100))  # Opcional, como se escribe en ingles??? 
    affiliate_number = db.Column(db.String(50), unique=True, nullable=False)

    is_volunteer = db.Column(db.Boolean, nullable=False)    # puede ser Voluntario o Personal rentado, se describe con un boolean.

    enabled = db.Column(db.Boolean, default=True, nullable=False)

    # Relacion con la tabla de User (opcional)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='employee', lazy=True, foreign_keys=[user_id])

    # Relación con la documentación complementaria
    employee_documents = db.relationship("EmployeeDocument", back_populates="employee")
    documents = db.relationship("Document", secondary="employee_documents", viewonly=True)

    received_collections = db.relationship('Collection',
                                        back_populates='received_by',
                                        cascade='all, delete-orphan')
    payments = db.relationship('Payment',
                             back_populates='beneficiary',
                             cascade='all, delete-orphan')

    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Relacion con los caballos que le fueron asignados
    horses = db.relationship('Horse', secondary='horses_employees', back_populates='employees')

    def __init__(self, name: str, surname: str, dni: str, address_id: int, email: str, locality_id: int, phone: str, profession_id: int,
                job_position_id: int, emergency_contact_name: str, emergency_contact_phone: str, obra_social: str, affiliate_number: str,
                is_volunteer: bool, enabled: bool = True, user_id: Optional[int] = None, start_date: datetime = datetime.now(), end_date: Optional[datetime] = None):
        self.name = name
        self.surname = surname
        self.dni = dni
        self.address_id = address_id
        self.email = email
        self.locality_id = locality_id
        self.phone = phone
        self.profession_id = profession_id
        self.job_position_id = job_position_id
        self.start_date = datetime.now().date()
        self.end_date = None
        self.emergency_contact_name = emergency_contact_name
        self.emergency_contact_phone = emergency_contact_phone
        self.obra_social = obra_social
        self.affiliate_number = affiliate_number
        self.is_volunteer = is_volunteer
        self.enabled = enabled
        self.user_id = user_id
        self.start_date = start_date
        if (end_date != ""):
            self.end_date = end_date

    def __repr__(self):
        return f'<Employee {self.name} {self.surname}>'


