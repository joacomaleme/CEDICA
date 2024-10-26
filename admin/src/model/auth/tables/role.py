from src.model.database import db
from src.model.auth.tables.role_permissions import role_permissions


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    
    # relacion 1 a N, un usuario tiene un unico rol y un rol muchos usuarios
    users = db.relationship('User', back_populates='role')

    # relacion N a N, un rol tiene muchos permisos y un permiso es tenido por muchos roles
    permissions = db.relationship('Permission', secondary=role_permissions, back_populates='roles') # el atributo back_populates es para indicar que ambas tablas pueden acceder a la otra via atributos y el atributo secondary define una relacion N a N.

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<Role {self.name}>"
