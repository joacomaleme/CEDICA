from src.model.database import db
from src.model.auth.tables.user import User
from src.model.auth.tables.role import Role
from sqlalchemy.orm  import Query
from typing import List, Optional


def create_user(email: str, alias: str, password: str, role_id:Optional[int] = None, enabled:bool = True, system_admin:bool = False) -> User:
    user = User(email, alias, password, role_id, enabled, system_admin)
    db.session.add(user)
    db.session.commit()
    db.session.expunge(user)
    return user

def list_users():   # lista TODOS los usuarios (solo usar cuando sea estrictamente necesario)
    users = User.query.all()
    [db.session.expunge(user) for user in users.items]
    return users # puede devolver una lista vacia

def get_user(id: int):      #devuelve un usuario dado un id
    user = User.query.get(id)
    db.session.expunge(user)
    return user # si no encuentra nada devuelve None

def get_user_by_email(email: str):      #devuelve un usuario dado un email (el email es unico)
    user = User.query.filter(User.email == email).first()
    db.session.expunge(user)
    return user # si no encuentra nada devuelve None

def __update_user__(to_update: User) -> User:
    user = User.query.get(to_update.id)
    if user is None:
        raise ValueError("No se encontro un usuario con ese ID") 
    user.email = to_update.email or user.email
    user.alias = to_update.alias or user.alias
    user.password = to_update.password or user.password
    user.enabled = to_update.enabled if to_update.enabled is not None else user.enabled
    user.system_admin = to_update.system_admin if to_update.system_admin is not None else user.system_admin
    user.role = to_update.role #debería en vez solo copiar la foreign key? En el video lo hacen así
    db.session.commit()
    db.session.expunge(user)
    return user

def delete_user(id: int):   # creo que no hace falta excepcion aca
    user = User.query.get(id)
    if user is None:
        raise ValueError("No se encontro un usuario con ese ID")
    db.session.delete(user)
    db.session.commit()

###INSTRUCCIONES DE UPDATE ESPECÍFICAS

def toggle_block(id: int) -> User:
    user = User.query.get(id)
    if user is None:
        raise ValueError("No se encontro un usuario con ese ID") 
    if user.system_admin == False:
        user.enabled = not user.enabled
        db.session.commit()
    else:
        raise PermissionError("No se permite bloquear a administradores del sistema")
    db.session.expunge(user)
    return user

def assign_role(id: int, role: Optional[Role] = None) -> User: #Enviar role = None o sin parametro para remover rol.
    user = User.query.get(id)
    if user is None:
        raise ValueError("No se encontro un usuario con ese ID")
    if user.system_admin == False:
        user.role = role
        db.session.commit()
    else:
        raise PermissionError("No se permite asignar roles a administradores del sistema")
    db.session.expunge(user)
    return user

###INSTRUCCIONES DE LISTADO ESPECÍFICAS

def sorted_by_attribute(users: Query, attribute:str = "email", ascending:bool = True) -> Query:
    return users.order_by(getattr(User, attribute).asc() if ascending else getattr(User, users).desc()) #Solo enviar parametros "email" o "inserted_at"

def filter_active(users:Query, show_enabled:bool = True, show_disabled:bool = True) -> Query:
    return users.filter(db.or_((User.enabled == show_enabled), (User.enabled == (not show_disabled))))

def filter_rol(users:Query, roles:List[Role]) -> Query:
    return users.filter(User.role.id.in_(role.id for role in roles))

def search_by_mail(users:Query, email:str = "") -> Query:
    return users.filter(User.email.ilike(f"%{email}%"))

def get_filtered_list(page:int, limit:int = 25, show_enabled:bool = True, show_disabled:bool = True, roles:List[Role] = [], sort_attr:str = "email", ascending:bool = True, search_mail:str = ""):
    if roles == []:
        roles = Role.query.all()
    user_list = search_by_mail(\
                    sorted_by_attribute(\
                        filter_rol(\
                            filter_active(User.query, show_enabled, show_disabled), roles), sort_attr, ascending), search_mail)\
                                .paginate(page=page, per_page=limit, error_out=False)
    [db.session.expunge(user) for user in user_list.items]
    return user_list