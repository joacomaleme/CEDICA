from src.model.database import db

#Esta es la tabla de asociacion para la relacion N a N entre la roles y permisos
role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.BigInteger, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.BigInteger, db.ForeignKey('permissions.id'), primary_key=True)
) 
