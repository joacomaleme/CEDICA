from datetime import datetime
from src.model.database import db

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(16), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)       # podria ser otra tabla
    email = db.Column(db.String(120), unique=True, nullable=False)
    locality = db.Column(db.String(100), nullable=False)    # podria ser otra tabla
    phone = db.Column(db.String(20), nullable=False)
    
    # Relación con Profession
    profession_id = db.Column(db.BigInteger, db.ForeignKey('professions.id'), nullable=False)
    profession = db.relationship('Profession')

    # Relación con JobPosition
    job_position_id = db.Column(db.BigInteger, db.ForeignKey('job_positions.id'), nullable=False)
    job_position = db.relationship('JobPosition')


    start_date = db.Column(db.Date, nullable=False, default=datetime.now())
    end_date = db.Column(db.Date)

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

    def __repr__(self):
        return f'<Employee {self.nombre} {self.apellido}>'


