from src.model.database import db
from datetime import datetime
from src.model.generic.tables.document_types import DocumentType  # Ensure this is imported
from src.model.riders.tables.rider import Rider  # Ensure this is imported

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    type_id = db.Column(db.BigInteger, db.ForeignKey('document_types.id'), nullable=False)  # Relacion con la tabla de tipo de docs
    type = db.relationship('DocumentType', back_populates='documents')
    format = db.Column(db.String(10), nullable=False) # No se si el formato es necesario
    upload_date = db.Column(db.DateTime, nullable = False)
    is_external = db.Column(db.Boolean, nullable=False) # Si el archivo se guarda en un link externo a la pagina o no. (si es interno se almacena con MinIO)
    allowed_operations = db.Column(db.String(20), nullable=False) # Esto podria ser otra tabla aparte
    file_address = db.Column(db.String(255), nullable=False)  # Ruta al archivo almacenado

    # Relaciones con las entidades Employee y Rider
    employee_id = db.Column(db.BigInteger, db.ForeignKey('employees.id'), nullable=True)
    employee = db.relationship('Employee', back_populates='documents')
    rider_id = db.Column(db.BigInteger, db.ForeignKey('riders.id'), nullable=True)
    rider = db.relationship('Rider', back_populates='documents')

    def __init__(self, title: str, type_id: int, format: str, upload_date: datetime, is_external: bool, allowed_operations: str, file_address: str, employee_id, rider_id):
        self.title = title
        self.type_id = type_id
        self.format = format
        self.upload_date = upload_date
        self.is_external = is_external
        self.allowed_operations = allowed_operations
        self.file_address = file_address
        self.employee_id = employee_id
        self.rider_id = rider_id

    def __repr__(self):
        return f'<Document {self.titulo} ({self.tipo})>'
