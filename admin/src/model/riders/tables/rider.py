from datetime import date
from datetime import datetime
from src.model.database import db
from src.model.riders.tables.family_allowance_type import FamilyAllowanceType
from src.model.riders.tables.disability_diagnosis import DisabilityDiagnosis
from src.model.riders.tables.disability_type import DisabilityType
from src.model.riders.tables.rider_guardian import RiderGuardian
from src.model.riders.tables.pension_type import PensionType
from src.model.riders.tables.school import School
from src.model.horses.tables.horse import Horse
from src.model.riders.tables.rider_document import RiderDocument
from src.model.generic.tables.work_proposal import WorkProposal
from src.model.generic.tables.sede import Sede

class Rider(db.Model):  # Representa Jinetes y Amazonas (J&A)
    __tablename__ = 'riders'

    # Identificador único del registro
    id = db.Column(db.BigInteger, primary_key=True)

    # Información básica del J&A
    name = db.Column(db.String(100), nullable=False)  # Nombre del jinete o amazona
    last_name = db.Column(db.String(100), nullable=False)  # Apellido del jinete o amazona
    dni = db.Column(db.String(16), unique=True, nullable=False)  # Documento de identidad único
    age = db.Column(db.Integer, nullable=False)  # Edad actual calculada

    # Información de nacimiento
    birth_date = db.Column(db.Date, nullable=False)  # Fecha de nacimiento
    birth_locality_id = db.Column(db.BigInteger, db.ForeignKey('localities.id'), nullable=False) # Localidad de nacimiento
    birth_locality = db.relationship('Locality', backref='birth_riders', foreign_keys=[birth_locality_id])
    birth_province_id = db.Column(db.BigInteger, db.ForeignKey('provinces.id'), nullable=False) # Provincia de nacimiento
    birth_province = db.relationship('Province', backref='birth_riders', foreign_keys=[birth_province_id])

    # Dirección actual del J&A
    address_id = db.Column(db.BigInteger, db.ForeignKey('addresses.id'), nullable=False)
    address = db.relationship('Address', foreign_keys=[address_id])

    # Localidad y provincia actuales del J&A
    current_locality_id = db.Column(db.BigInteger, db.ForeignKey('localities.id'), nullable=False)  # Localidad actual
    current_locality = db.relationship('Locality', backref='current_riders', foreign_keys=[current_locality_id])
    current_province_id = db.Column(db.BigInteger, db.ForeignKey('provinces.id'), nullable=False)   # Provincia actual
    current_province = db.relationship('Province', backref='current_riders', foreign_keys=[current_province_id])

    # Información de contacto
    phone = db.Column(db.String(20), nullable=False)  # Teléfono actual
    emergency_contact_name = db.Column(db.String(100), nullable=False)  # Contacto de emergencia
    emergency_contact_phone = db.Column(db.String(20), nullable=False)  # Teléfono del contacto de emergencia

    # Información de beca--
    has_scholarship = db.Column(db.Boolean, nullable=False, default=False)  # Si está becado o no
    scholarship_percentage = db.Column(db.Float)  # Porcentaje de la beca (si aplica)

    # Información sobre discapacidad
    has_disability_certificate = db.Column(db.Boolean, nullable=False, default=False)  # Certificado de discapacidad
    disability_diagnosis_id = db.Column(db.BigInteger, db.ForeignKey('disability_diagnoses.id'), nullable=True)
    disability_diagnosis = db.relationship('DisabilityDiagnosis', backref='current_riders', foreign_keys=[disability_diagnosis_id])  # Diagnóstico de la discapacidad
    disability_type_id = db.Column(db.BigInteger, db.ForeignKey('disability_types.id'), nullable=True)
    disability_type = db.relationship('DisabilityType', backref='current_riders', foreign_keys=[disability_type_id])

    # Información sobre asignaciones familiares
    receives_family_allowance = db.Column(db.Boolean, nullable=False, default=False)  # Si recibe asignaciones familiares

    family_allowance_type_id = db.Column(db.BigInteger, db.ForeignKey('family_allowance_types.id'))# Tipo de asignación: Universal, Discapacidad, Escolar
    family_allowance_type = db.relationship('FamilyAllowanceType', foreign_keys=[family_allowance_type_id])
    receives_pension = db.Column(db.Boolean, nullable=False, default=False)  # Si recibe pensión o no
    pension_type_id = db.Column(db.BigInteger, db.ForeignKey('pension_types.id'))
    pension_type = db.relationship('PensionType', back_populates='riders', foreign_keys=[pension_type_id])


    # Información sobre la obra social y salud
    health_insurance = db.Column(db.String(100))  # Obra social del alumno
    affiliate_number = db.Column(db.String(50))  # Número de afiliado
    has_guardianship = db.Column(db.Boolean, nullable=False, default=False)  # Si tiene curatela

    # Información escolar
    school_id = db.Column(db.BigInteger, db.ForeignKey('schools.id'))
    school = db.relationship('School', backref='riders', foreign_keys=[school_id])
    current_grade = db.Column(db.String(50))  # Grado o año escolar actual


    attending_professionals = db.Column(db.Text)  # Profesionales que lo atienden (campo libre)

    # Padre/Madre/Tutor, relacion N a N.

    guardians = db.relationship('Guardian', secondary='rider_guardians', back_populates='riders')

    # Información sobre el trabajo en la la institución
    work_proposal_id = db.Column(db.BigInteger, db.ForeignKey('work_proposals.id'))
    work_proposal = db.relationship('WorkProposal', foreign_keys=[work_proposal_id])
    active = db.Column(db.Boolean, nullable=False)
    sede_id = db.Column(db.BigInteger, db.ForeignKey('sedes.id'))
    sede = db.relationship('Sede', foreign_keys=[sede_id])
    # Relacion N a N con WorkDay
    work_days = db.relationship('WorkDay', secondary='rider_work_day', back_populates='riders')

    teacher_id = db.Column(db.BigInteger, db.ForeignKey('employees.id'))  # Profesor/Terapeuta 
    teacher = db.relationship('Employee', foreign_keys=[teacher_id])
    horse_conductor_id = db.Column(db.BigInteger, db.ForeignKey('employees.id'))  # Conductor/a del caballo
    horse_conductor = db.relationship('Employee', foreign_keys=[horse_conductor_id])
    horse_id = db.Column(db.BigInteger, db.ForeignKey('horses.id'))  # Caballo
    horse = db.relationship('Horse', backref='riders', foreign_keys=[horse_id])

    track_assistant_id = db.Column(db.BigInteger, db.ForeignKey('employees.id'))  # Auxiliar de pista
    track_assistant = db.relationship('Employee', foreign_keys=[track_assistant_id])

    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Relacion con sus Documentos
    rider_documents = db.relationship("RiderDocument", back_populates="rider")
    documents = db.relationship("Document", secondary="rider_documents", viewonly=True)


    # Informacion sobre su deuda
    is_indebt = db.Column(db.Boolean, nullable = False, default=False)
    debt = db.Column(db.Float, nullable=False, default=0.0)


    def __init__(self, name, last_name, dni, age, birth_date, birth_locality_id, birth_province_id, address_id, current_locality_id, current_province_id, phone, emergency_contact_name, emergency_contact_phone, active, sede_id, has_scholarship=False, scholarship_percentage=None, has_disability_certificate=False, disability_diagnosis_id=None, disability_type_id=None, receives_family_allowance=False, family_allowance_type_id=None, receives_pension=False, pension_type_id=None, health_insurance=None, affiliate_number=None, has_guardianship=False, school_id=None, current_grade=None, attending_professionals=None, work_proposal_id=None, teacher_id=None, horse_conductor_id=None, horse_id=None, track_assistant_id=None, is_indebt=False, debt=0.0):
        self.name = name
        self.last_name = last_name
        self.dni = dni
        self.age = age
        self.birth_date = birth_date
        self.birth_locality_id = birth_locality_id
        self.birth_province_id = birth_province_id
        self.address_id = address_id
        self.current_locality_id = current_locality_id
        self.current_province_id = current_province_id
        self.phone = phone
        self.emergency_contact_name = emergency_contact_name
        self.emergency_contact_phone = emergency_contact_phone
        self.active = active
        self.sede_id = sede_id
        self.has_scholarship = has_scholarship
        self.scholarship_percentage = scholarship_percentage
        self.has_disability_certificate = has_disability_certificate
        self.disability_diagnosis_id = disability_diagnosis_id
        self.disability_type_id = disability_type_id
        self.receives_family_allowance = receives_family_allowance
        self.family_allowance_type_id = family_allowance_type_id
        self.receives_pension = receives_pension
        self.pension_type_id = pension_type_id
        self.health_insurance = health_insurance
        self.affiliate_number = affiliate_number
        self.has_guardianship = has_guardianship
        self.school_id = school_id
        self.current_grade = current_grade
        self.attending_professionals = attending_professionals
        self.work_proposal_id = work_proposal_id
        self.teacher_id = teacher_id
        self.horse_conductor_id = horse_conductor_id
        self.horse_id = horse_id
        self.track_assistant_id = track_assistant_id
        self.is_indebt = is_indebt
        self.debt = debt


    # Definición de cómo se muestra la instancia al llamarla
    def __repr__(self):
        return f'<Rider {self.name} {self.last_name}>'

