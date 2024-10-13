from src.model.database import db
from src.model.auth.tables.permission import Permission


def create_permission(name:str) -> Permission:
    permission = Permission(name)
    db.session.add(permission)
    db.session.commit()
    db.session.expunge(permission)
    return permission
