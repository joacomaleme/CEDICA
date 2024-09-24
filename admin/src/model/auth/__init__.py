from src.model.database import db
from .user import User
from .role import Role
from .permission import Permission
from .role_permissions import role_permissions

def create_user(**kwargs):  #checkear tema args, se podria pasar un User o una lista definida de atributos
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user

def list_users():
    users = User.query.all()
    
    return users

def get_user(id: int):
    user = User.query.get(id) #si no encuentra al user tira 404

    return user.to_dict()

def update_user(): 
    db.session.commit()     #solo se hace commit pq el objeto se cambia por afuera??
    
    return True         # devuelve true pq ns que devolver
    
def delete_user(id: int):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user     #deberia devolver otra cosa?

def create_role(**kwargs):
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()

def create_permission(**kwargs):
    permission = Permission(**kwargs)
    db.session.add(permission)
    db.session.commit()
