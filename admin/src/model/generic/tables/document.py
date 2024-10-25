from src.model.database import db
from typing import Optional
from datetime import datetime

class Document(db.Model):
    from src.model.generic.tables.document_types import DocumentType  # Ensure this is imported
    from src.model.riders.tables.rider import Rider  # Ensure this is imported

    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), nullable=False)
    type_id = db.Column(db.BigInteger, db.ForeignKey('document_types.id'), nullable=True)  # Relacion con la tabla de tipo de docs
    type = db.relationship('DocumentType', back_populates='documents', lazy="joined")
    format = db.Column(db.String(100), nullable=False) # No se si el formato es necesario
    upload_date = db.Column(db.DateTime, nullable = False, default=datetime.now())
    is_external = db.Column(db.Boolean, nullable=False) # Si el archivo se guarda en un link externo a la pagina o no. (si es interno se almacena con MinIO)
    allowed_operations = db.Column(db.String(20), nullable=False) # Esto podria ser otra tabla aparte
    file_address = db.Column(db.String(512), nullable=False)  # Ruta al archivo almacenado

    def __init__(self, title: str, format: str, is_external: bool, allowed_operations: str, file_address: str, type_id: Optional[int]=None, upload_date: datetime = datetime.now()):
        self.title = title
        self.type_id = type_id
        self.format = format
        self.upload_date = upload_date
        self.is_external = is_external
        self.allowed_operations = allowed_operations
        self.file_address = file_address


    def __repr__(self):
        return f'<Document {self.title} ({self.type})>'
