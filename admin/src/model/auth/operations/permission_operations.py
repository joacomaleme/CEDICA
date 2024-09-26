from src.model.database import db
from ..tables.permission import Permission

def create_permission(name:str):
    permission = Permission(name)
    db.session.add(permission)
    db.session.commit()