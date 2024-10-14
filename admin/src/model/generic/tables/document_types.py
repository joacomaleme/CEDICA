from src.model.database import db

"""
    Tipo de documento (Título, DNI, CV)  En la consigna se nombran:
    entrevista | evaluación | planificaciones | evolución | crónicas | documental
"""

class DocumentType(db.Model):
    __tablename__ = 'document_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    documents = db.relationship('Document', back_populates='type')

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'<DocumentType {self.name}>'
