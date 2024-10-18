from src.model.database import db
from src.model.encrypt import bcrypt
from src.model.auth.tables.user import User
from src.model.auth.tables.role import Role
from .role_operations import search_name
from sqlalchemy.orm  import Query
from typing import List, Optional


def create_user(email: str, alias: str, password: str, role_id:Optional[int] = None, enabled:bool = True) -> User:
    user = User(email, alias, bcrypt.generate_password_hash(password.encode("utf-8")).decode("utf-8"), role_id, enabled)
    db.session.add(user)
    db.session.commit()
    db.session.expunge(user)
    return user

def list_users() -> List[User]:   # lista TODOS los usuarios (solo usar cuando sea estrictamente necesario)
    users = User.query.all()
    [db.session.expunge(user) for user in users]
    return users # puede devolver una lista vacia

def get_user(id: int) -> User:      #devuelve un usuario dado un id
    user = User.query.get(id)
    if user:
        db.session.expunge(user)
    return user # si no encuentra nada devuelve None

def get_user_by_email(email: str) -> User:      #devuelve un usuario dado un email (el email es unico)
    user = User.query.filter(User.email == email).first()
    if user:
        db.session.expunge(user)
    return user # si no encuentra nada devuelve None

def get_user_by_alias(alias: str) -> User:
    user = User.query.filter(User.alias == alias).first()
    if user:
        db.session.expunge(user)
    return user

def authenticate_user(email: str, password: str) -> User:
    user = get_user_by_email(email)
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return None
    

def update_user(to_update: User) -> User:
    user = User.query.get(to_update.id)
    if not user:
        raise ValueError("No se encontro un usuario con ese ID") 
    user.email = to_update.email
    user.alias = to_update.alias
    user.password = bcrypt.generate_password_hash(to_update.password.encode("utf-8")).decode("utf-8") if to_update.password else user.password
    user.enabled = to_update.enabled
    user.role_id = to_update.role_id
    db.session.commit()
    db.session.expunge(user)
    return user

def delete_user(id: int) -> bool:   # creo que no hace falta excepcion aca
    user = User.query.get(id)
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    return True

###INSTRUCCIONES DE UPDATE ESPECÍFICAS

def toggle_block(id: int) -> User:
    user = User.query.get(id)
    if not user:
        raise ValueError("No se encontro un usuario con ese ID") 
    if user.role == False:
        user.enabled = not user.enabled
        db.session.commit()
    else:
        raise PermissionError("No se permite bloquear a administradores del sistema")
    db.session.expunge(user)
    return user

def assign_role(id: int, role: Optional[Role] = None) -> User: #Enviar role = None o sin parametro para remover rol.
    user = User.query.get(id)
    if not user:
        raise ValueError("No se encontro un usuario con ese ID")
    if user.system_admin == False:
        user.role = role
        db.session.commit()
    else:
        raise PermissionError("No se permite asignar roles a administradores del sistema")
    db.session.expunge(user)
    return user

### CHECKEO DE PERMISOS

def has_permission(user_email: str, permission_name:str) -> bool:
    # verifica que el rol del usuario tenga el permiso especificado
    user = get_user_by_email(user_email)
    if user:
        role = Role.query.get(user.role_id)
        if role:
            return any(permission.name == permission_name for permission in role.permissions)
        else:
            return False
    else:
        return False

###INSTRUCCIONES DE LISTADO ESPECÍFICAS


def start_query():
    return User.query

def sorted_by_attribute(users: Query, attribute:str = "email", ascending:bool = True) -> Query:
    return users.order_by(getattr(User, attribute).asc() if ascending else getattr(User, attribute).desc()) #Solo enviar parametros "email" o "inserted_at"

def filter_active(users:Query, show_enabled:bool = True) -> Query:
    return users.filter(User.enabled == show_enabled)

def filter_role(users:Query, role_name:str) -> Query:
    role = search_name(role_name)
    if role:
        return users.filter(db.and_(User.role_id.isnot(None), User.role_id == role.id))
    else:
        return users

def search_by_mail(users:Query, email:str = "") -> Query:
    return users.filter(User.email.ilike(f"%{email}%"))

def get_paginated_list(users:Query, page:int, limit:int = 25) -> List[User]:
    user_list = users.paginate(page=page, per_page=limit, error_out=False)
    [db.session.expunge(user) for user in user_list]
    return [user_list, ((users.count()-1)//limit)+1]
