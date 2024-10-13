from src.model.database import db

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Tipo de documento (Título, DNI, CV) // checkear
    archivo = db.Column(db.String(255), nullable=False)  # Ruta al archivo almacenado

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)

    def __repr__(self):
        return f'<Document {self.titulo} ({self.tipo})>'
