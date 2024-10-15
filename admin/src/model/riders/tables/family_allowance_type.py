from src.model.database import db

"""
    Tabla que representa a los tipos de asignacion familiar, en la consigna se nombran:
    Asignacion Universal por Hijo, Asignacion Universal por hijo con Discapacidad, Asignacion por ayuda escolar anual.
"""

class FamilyAllowanceType(db.Model):
    __tablename__ = 'family_allowance_types'

    id = db.Column(db.BigInteger, primary_key=True)  # Identificador único
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f'<FamilyAllowanceType {self.name}>'
