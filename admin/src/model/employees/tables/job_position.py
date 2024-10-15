from src.model.database import db

"""
'Administrativo/a', 'Terapeuta', 'Conductor', 'Auxiliar de pista', 
'Herrero', 'Veterinario', 'Entrenador de Caballos', 'Domador', 
'Profesor de Equitación', 'Docente de Capacitación', 
'Auxiliar de mantenimiento', 'Otro'.
"""

class JobPosition(db.Model):
    __tablename__ = 'job_positions'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Relación inversa con Employee
    employees = db.relationship('Employee', backref='job_position', lazy=True)

    def __init__(self, name: str):
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def __repr__(self):
        return f'<JobPosition {self.name}>'
