from datetime import datetime
from src.model.database import db
from src.model.employees.tables.document import Document  # Ensure this is imported
from src.model.employees.tables.job_position import JobPosition  # Ensure this is imported
from src.model.employees.tables.profession import Profession  # Ensure this is imported

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(255), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)       # podria ser otra tabla
    email = db.Column(db.String(120), unique=True, nullable=False)
    locality = db.Column(db.String(100), nullable=False)    # podria ser otra tabla
    phone = db.Column(db.String(20), nullable=False)
    
    # Relación con Profession
    profession_id = db.Column(db.BigInteger, db.ForeignKey('professions.id'), nullable=False)

    # Relación con JobPosition
    job_position_id = db.Column(db.BigInteger, db.ForeignKey('job_positions.id'), nullable=False)

    start_date = db.Column(db.Date, nullable=False, default=datetime.now())
    end_date = db.Column(db.Date, default=None)

    emergency_contact_name = db.Column(db.String(100), nullable=False)
    emergency_contact_phone = db.Column(db.String(20), nullable=False)

    obra_social = db.Column(db.String(100))  # Opcional, como se escribe en ingles??? 
    affiliate_number = db.Column(db.String(50))

    is_volunteer = db.Column(db.Boolean, nullable=False)    # puede ser Voluntario o Personal rentado, se describe con un boolean.

    enabled = db.Column(db.Boolean, default=True, nullable=False)

    # Relacion con la tabla de User (opcional)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='employee', lazy=True)

    # Relación con la documentación complementaria
    documents = db.relationship('Document', backref='employee', lazy=True)

    payments = db.relationship('Payment', back_populates='beneficiary')

    def __init__(self, name: str, surname: str, dni: str, address: str, email: str, locality: str, phone: str, profession_id: int, 
                job_position_id: int, emergency_contact_name: str, emergency_contact_phone: str, obra_social: str, affiliate_number: str,
                is_volunteer: bool = False, enabled: bool = True, user_id=None, start_date: datetime = datetime.now(), end_date: datetime=None):
        self.name = name
        self.surname = surname
        self.dni = dni
        self.address = address
        self.email = email
        self.locality = locality
        self.phone = phone
        self.profession_id = profession_id
        self.job_position_id = job_position_id
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


