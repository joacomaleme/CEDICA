from src.model.database import db
from ..tables.permission import Permission
from copy import deepcopy


def create_permission(name:str) -> Permission:
    permission = Permission(name)
    db.session.add(permission)
    db.session.commit()

    return deepcopy(permission)
