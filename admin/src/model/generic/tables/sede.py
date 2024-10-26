from src.model.database import db

"""
    Las sedes de la consigna son: CASJ, HLP, OTRO
"""

class Sede(db.Model):
    __tablename__ = 'sedes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name
