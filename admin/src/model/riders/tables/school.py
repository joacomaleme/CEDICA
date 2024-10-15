from src.model.database import db
from typing import Optional

class School(db.Model):  # Tabla para Instituciones Escolares
    __tablename__ = 'schools'

    id = db.Column(db.BigInteger, primary_key=True)  # Identificador único
    name = db.Column(db.String(255), nullable=False)  # Nombre de la escuela
    address = db.Column(db.String(255), nullable=False)  # Dirección completa
    phone = db.Column(db.String(20), nullable=False)  # Número de teléfono
    observations = db.Column(db.Text)  # Observaciones adicionales

    def __init__(self, name: str, address: str, phone: str, observations: Optional[str] = None):
        self.name = name
        self.address = address
        self.phone = phone
        self.observations = observations

    def __repr__(self):
        return f'<School {self.name}>'
