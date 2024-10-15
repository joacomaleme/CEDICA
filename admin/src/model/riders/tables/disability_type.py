from src.model.database import db

"""
    Tabla que representa a los distintos TIPOS de discapacidades, en la consigna se nombran:
    Mental, Motora, Sensorial, Visceral.
"""

class DisabilityType(db.Model):
    __tablename__ = 'disability_types'

    id = db.Column(db.BigInteger, primary_key=True)  # Identificador único
    type = db.Column(db.String(255), nullable=False, unique=True)  # Nombre del tipo (Mental, Motora, Sensorial, Visceral)

    def __repr__(self):
        return f'<DisabilityType {self.diagnosis}>'
