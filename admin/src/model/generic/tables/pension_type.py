from src.model.database import db

class PensionType(db.Model):  # Tabla para Tipos de Pensión
    __tablename__ = 'pension_types'

    id = db.Column(db.BigInteger, primary_key=True)  # Identificador único
    name = db.Column(db.String(50), nullable=False, unique=True)  # Nombre de la pensión (Provincial, Nacional)

    def __repr__(self):
        return f'<PensionType {self.name}>'

