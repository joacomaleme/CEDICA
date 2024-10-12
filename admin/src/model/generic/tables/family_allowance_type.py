from src.model.database import db

class FamilyAllowanceType(db.Model):  # Tabla para Tipos de Asignación Familiar
    __tablename__ = 'family_allowance_types'

    id = db.Column(db.BigInteger, primary_key=True)  # Identificador único
    name = db.Column(db.String(100), nullable=False, unique=True)  # Nombre de la asignación (Asignación Universal, AUH con discapacidad, Ayuda escolar)

    def __repr__(self):
        return f'<FamilyAllowanceType {self.name}>'
