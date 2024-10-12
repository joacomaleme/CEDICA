from src.model.database import db

class School(db.Model):  # Tabla para Instituciones Escolares
    __tablename__ = 'schools'

    id = db.Column(db.BigInteger, primary_key=True)  # Identificador único
    name = db.Column(db.String(255), nullable=False)  # Nombre de la escuela
    address = db.Column(db.String(255), nullable=False)  # Dirección completa
    phone = db.Column(db.String(20), nullable=False)  # Número de teléfono
    observations = db.Column(db.Text)  # Observaciones adicionales

    def __repr__(self):
        return f'<School {self.name}>'
