from src.model.database import db

class DisabilityType(db.Model):  # Tabla para Tipos de Discapacidades
    __tablename__ = 'disability_types'

    id = db.Column(db.BigInteger, primary_key=True)  # Identificador único
    type = db.Column(db.String(255), nullable=False, unique=True)  # Nombre del tipo (Mental, Motora, Sensorial, Visceral)

    def __repr__(self):
        return f'<DisabilityType {self.diagnosis}>'
