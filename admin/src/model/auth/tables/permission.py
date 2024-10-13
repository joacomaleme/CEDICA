from src.model.database import db
from src.model.auth.tables.role_permissions import role_permissions


class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    # relacion N a N, un permiso puede pertenecer a muchos roles y un rol tener muchos permisos
    roles = db.relationship('Role', secondary=role_permissions, back_populates='permissions')

    def __init__(self, name:str):
        self.name = name

    def __repr__(self):
        return f"<Permission {self.name}>"
