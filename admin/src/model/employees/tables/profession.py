from src.model.database import db

"""
'Psicólogo/a', 'Psicomotricista', 'Médico/a', 'Kinesiólogo/a', 'Terapista Ocupacional', 
'Psicopedagogo/a', 'Docente', 'Profesor', 'Fonoaudiólogo/a', 'Veterinario/a', 'Otro'.
"""

class Profession(db.Model):
    __tablename__ = 'professions'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Relación inversa con Employee
    employees = db.relationship('Employee', back_populates='profession')

    def __init__(self, name: str):
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def __repr__(self):
        return f'<Profesion {self.name}>'
