from src.model.database import db

"""
    Tabla que representa las posibles propuestas laborales ofrecidas por la institucion.
    En la consigna se nombran:
    Hipoterapia – Monta Terapéutica – Deporte Ecuestre Adaptado – Actividades Recreativas - Equitación
"""

class WorkProposal(db.Model):
    __tablename__ = 'work_proposals'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, name, active=True):
        self.name = name 
        self.active = active
