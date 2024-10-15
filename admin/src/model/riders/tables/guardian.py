from src.model.database import db
from src.model.riders.tables.rider_guardian import rider_guardians

class Guardian(db.Model):
    __tablename__ = 'guardians'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(16), unique=True, nullable=False)

    # Información de domicilio
    address_id = db.Column(db.BigInteger, db.ForeignKey('addresses.id'), nullable=False)
    address = db.relationship('Address', foreign_keys=[address_id])
    locality_id = db.Column(db.BigInteger, db.ForeignKey('localities.id'), nullable=False)
    locality = db.relationship('Locality', foreign_keys=[locality_id])
    province_id = db.Column(db.BigInteger, db.ForeignKey('provinces.id'), nullable=False)
    province = db.relationship('Province', foreign_keys=[province_id])

    # Contacto
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    # Nivel de escolaridad (Primario, Secundario, Terciario, Universitario)
    education_level = db.Column(db.String(50), nullable=False)

    # Actividad u ocupación del familiar/tutor
    occupation = db.Column(db.String(100), nullable=False)

    riders = db.relationship('Rider', secondary='rider_guardians', back_populates='guardians')


    def __init__(self, name: str, last_name: str, dni: int, address_id: int, locality_id: int, province_id: int, phone: str, email: str, education_level: str, occupation: str):
        self.name = name
        self.last_name = last_name
        self.dni = dni
        self.address_id = address_id
        self.locality_id = locality_id
        self.province_id = province_id
        self.phone = phone
        self.email = email
        self.education_level = education_level
        self.occupation = occupation
