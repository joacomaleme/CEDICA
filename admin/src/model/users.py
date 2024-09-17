from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    alias = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    activo = db.Column(db.String(2), nullable=False, default='SI')  # Either 'SI' or 'NO'
    
    # Enum for roles: Técnica, Ecuestre, Voluntariado, Administración
    roles = db.Column(db.Enum('Técnica', 'Ecuestre', 'Voluntariado', 'Administración', name='role_types'), nullable=False)

    def __repr__(self):
        return f'<User {self.alias}>'

