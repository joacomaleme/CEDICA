from datetime import datetime
from src.model.database import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    activo = db.Column(db.String(2), nullable=False, default='SI')  # Either 'SI' o 'NO'
    
    # Enum para los roles: Técnica, Ecuestre, Voluntariado, Administración
    rol = db.Column(db.Enum('Tecnica', 'Ecuestre', 'Voluntariado', 'Administracion', name='role_types'), nullable=False)

    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'<User #{self.id} alias="{self.alias}" activo="{self.activo}">'

