from src.model.database import db
from src.model.encrypt import bcrypt
from src.model.auth.tables.user import User
from src.model.auth.tables.role import Role
from .role_operations import search_name
from sqlalchemy.orm  import Query
from typing import List, Optional


def create_user(email: str, alias: str, password: str, role_id:Optional[int] = None, enabled:bool = True) -> User:
    '''
    Recibe un email (string), alias (string), contraseña (string), id de rol (integer opcional), booleano de activo/inactivo (bool opcional)
    En base a esos datos crea un nuevo usuario con esos parametros, a excepción de la contraseña que pasa un proceso de encriptación. 
    Luego retorna la instancia expurgada.
    '''
    user = User(email, alias, bcrypt.generate_password_hash(password.encode("utf-8")).decode("utf-8"), role_id, enabled)
    db.session.add(user)
    db.session.commit()
    db.session.expunge(user)
    return user

def list_users() -> List[User]:   # lista TODOS los usuarios (solo usar cuando sea estrictamente necesario)
    '''
    Retorna una lista de todos los usuarios como objetos, expurgados.
    '''
    users = User.query.all()
    [db.session.expunge(user) for user in users]
    return users # puede devolver una lista vacia

def get_user(id: int) -> User:      #devuelve un usuario dado un id
    '''
    Dado un id (integer), retorna el usuario al que le corresponde, expurgado, o None si la id no se haya en un usuario de la BD
    '''
    user = User.query.get(id)
    if user:
        db.session.expunge(user)
    return user # si no encuentra nada devuelve None

def get_user_by_email(email: str) -> User:      #devuelve un usuario dado un email (el email es unico)
    '''
    Dado un email (string), retorna el usuario al que le corresponde, expurgado, o None si el email no se haya en un usuario de la BD
    '''
    user = User.query.filter(User.email == email).first()
    if user:
        db.session.expunge(user)
    return user # si no encuentra nada devuelve None

def get_user_by_alias(alias: str) -> User:
    '''
    Dado un alias (string), retorna el usuario al que le corresponde, expurgado, o None si el alias no se haya en un usuario de la BD
    '''
    user = User.query.filter(User.alias == alias).first()
    if user:
        db.session.expunge(user)
    return user

def authenticate_user(email: str, password: str) -> User:
    '''
    Dado un email (string) y una contraseña encriptada (string), retorna el usuario al que le corresponden, expurgado,
    si y solo si a un usuario le corresponde tanto el mail como la contraseña, de forma contraria retorna None
    '''
    user = get_user_by_email(email)
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return None
    

def update_user(to_update: User) -> User:
    '''
    Dado un usuario, actualiza al usuario de misma id en la BD con los nuevos valores, y retorna al usuario modificado y expurgado.
    Si la ID no se encuentra lanza una excepción de valor.
    '''
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
    '''
    Dado un id (integer) elimina al usuario en la BD a quien le corresponde, si existiera, y retorna true. De no hayar al usuario a eliminar retornará false.
    '''
    user = User.query.get(id)
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    return True

### CHECKEO DE PERMISOS

def has_permission(user_email: str, permission_name:str) -> bool:
    '''
    Dado un email (string), y nombre de permiso (string), busca al usuario en la BD, su rol, y si tiene rol revisa si el permiso solicitado está activo para
    ese rol en particular. Retorna True si se encuentra al usuario, tiene rol, y ese rol cuenta con el permiso. False para todo otro escenario.
    '''
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
    '''Retorna un query de la lista User, función utilizada para encadenar con otras funciones de filtro'''
    return User.query

def sorted_by_attribute(users: Query, attribute:str = "email", ascending:bool = True) -> Query:
    '''
    Dado un Query, un atributo string opcional, que por norma interna debe ser "email" o "inserted_at", y un booleano opcional "ascending",
    retorna el Query ordenado por el atributo, ascendente o descendentemente dependiendo del booleano (True para ascendente)
    '''
    return users.order_by(getattr(User, attribute).asc() if ascending else getattr(User, attribute).desc()) #Solo enviar parametros "email" o "inserted_at"

def filter_active(users:Query, show_enabled:bool = True) -> Query:
    '''
    Dado un Query, y un booleano, retornan al Query filtrado conteniendo solo los usuarios desactivados para show_enabled=False, y solo activados para
    show_enabled=True
    '''
    return users.filter(User.enabled == show_enabled)

def filter_role(users:Query, role_name:str) -> Query:
    '''
    Dado un Query y un nombre de rol (string) retorna un Query con solo los usuarios que tienen ese rol asignado. Si el rol no se encuentra en la BD,
    se retornan todos los usuarios ya en el Query, indistintamente.
    '''
    role = search_name(role_name)
    if role:
        return users.filter(db.and_(User.role_id.isnot(None), User.role_id == role.id))
    else:
        return users

def search_by_mail(users:Query, email:str = "") -> Query:
    '''
    Dado un Query y un email (string), retorna un Query con solo los usuarios que contienen al email recibido como substring. No distingue mayúsculas.
    '''
    return users.filter(User.email.ilike(f"%{email}%"))

def get_num_pages(users:Query, limit:int = 25) -> int:
    '''
    Dado un Query y un límite de elementos por página, retorna cuantas páginas se crearían.
    '''
    return ((users.count()-1)//limit)+1

def get_paginated_list(users:Query, page:int, limit:int = 25) -> List[User]:
    '''
    Dado un Query, un número de página (integer), y un límite opcional (integer), retorna una lista con los usuarios correspondientes a
     la página solicitada.
    '''
    user_list = users.paginate(page=page, per_page=limit, error_out=False)
    [db.session.expunge(user) for user in user_list]
    return user_list
