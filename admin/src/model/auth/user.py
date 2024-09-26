from datetime import datetime
from src.model.database import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    alias = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    system_admin = db.Column(db.Boolean, nullable=False, default=False)
    role_id = db.Column(db.BigInteger, db.ForeignKey('roles.id'))
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    role = db.relationship('Role', back_populates='users')

    def __repr__(self):
        return f'<User #{self.id} alias="{self.alias}" activo="{self.enabled}">'
