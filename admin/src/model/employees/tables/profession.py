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
    employees = db.relationship('Employee', backref='profession', lazy=True)    # no se si esta hace falta tbh

    def __repr__(self):
        return f'<Profesion {self.nombre}>'
