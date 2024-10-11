from src.model.database import db

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    format = db.Column(db.String(50), nullable=False)  # Tipo de documento (Título, DNI, CV)
    file_address = db.Column(db.String(255), nullable=False)  # Ruta al archivo almacenado

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)  # puede ser innecesario.

    def __init__(self, titulo: str, tipo: str, archivo: str, employee_id: int):
        self.titulo = titulo
        self.tipo = tipo
        self.archivo = archivo
        self.employee_id = employee_id

    def __repr__(self):
        return f'<Document {self.titulo} ({self.tipo})>'
