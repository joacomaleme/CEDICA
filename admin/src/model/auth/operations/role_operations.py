from src.model.database import db
from ..tables.role import Role

def create_role(name:str):
    role = Role(name)
    db.session.add(role)
    db.session.commit()