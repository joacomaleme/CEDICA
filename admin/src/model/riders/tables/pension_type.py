from src.model.database import db

"""
    Tabla para la representacion de los tipos de pensiones, en la consigna se nombran:
    Provincial - Nacional
"""

class PensionType(db.Model):
    __tablename__ = 'pension_types'

    id = db.Column(db.BigInteger, primary_key=True)  # Identificador único
    name = db.Column(db.String(50), nullable=False, unique=True)


    riders = db.relationship('Rider', back_populates='pension_type')

    def __repr__(self):
        return f'<PensionType {self.name}>'

