from src.model.database import db
from .tables.user import User
from .tables.role import Role
from .tables.permission import Permission
from .tables.role_permissions import role_permissions

# para la administracion de permisos y para hacer el decorator
from functools import wraps # un decorator que hace que se mantengan los metadatos de la funcion cuando esta siendo decorada, util para debuggear.
from flask import abort, g

# CRUD 
'''
def create_user(**kwargs) -> User:  #checkear tema args, se podria pasar un User o una lista definida de atributos
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user

def list_users():   # lista TODOS los usuarios (solo usar cuando sea estrictamente necesario)
    users = User.query.all()

    return users # puede devolver una lista vacia

def list_users_filtered(enabled=None, role=None, order=None, direc='asc', page=1, limit=25):
    """
    Busca usuarios en la base de datos según los criterios especificados.

    :param active: Estado del usuario (bool) (opcional).
    :param role: Rol del usuario (opcional).
    :param order: Campo por el que ordenar (email | insertion_date) (opcional).
    :param direc: Dirección del ordenamiento (asc | desc) (por defecto: 'asc').
    :param page: Número de página para paginación (por defecto: 1) CHECKEAR.
    :param limit: Número máximo de registros por página (por defecto: 25).
    """
    if limit <= 0:      #se podria re-pensar si hay que usar excepciones o no
        raise ValueError("El limite debe ser mayor que 0.")
    if page <= 0:
        raise ValueError("La pagina debe ser mayor que 0.")

    users = User.query

    # filtros
    if enabled is not None:      # filtro por actividad
        users = users.filter(User.enabled == enabled)
    if role is not None:        # filtro por rol
        users = users.filter(User.role == role)     #NO se checkea el rol, si se escribe mal se va a devolver una lista vacia.

    # Ordenamiento
    if order is not None:
        if order == 'email':
            users = users.order_by(User.email.asc() if direc == 'asc' else User.email.desc())
        elif order == 'insertion_date':
            users = users.order_by(User.inserted_at.asc() if direc == 'asc' else User.inserted_at.desc())

    # Paginación seleccionando el numero de pagina y el limite de elementos.
    page_result = users.paginate(page=page, per_page=limit, error_out=False)    # error_out genera un error 404 si esta en true y se genera error de paginacion
    return page_result.items # Devuelve los resultados o lista vacia si no encuentra nada

def get_user(id: int):      #devuelve un usuario dado un id
    user = User.query.get(id)
    if User is None:
        raise ValueError("No se encontro un usuario con ese ID") 

    return user

def get_user_by_email(email: str):      #devuelve un usuario dado un email (el email es unico)
    user = User.query.filter(User.email == email).first()

    return user # si no encuentra nada devuelve None

def update_user(): 
    db.session.commit()     #solo se hace commit pq el objeto se cambia por afuera??

def delete_user(id: int):   # creo que no hace falta excepcion aca
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user


# funcionalidad para activar o desactivar a un usuario.

def block_user(id: int):
    user = get_user(id)
    if user is None:
        raise ValueError("No se encontro un usuario con ese ID") 
    if user.system_admin == False:
        user.enabled = False
    # else se podria hacer algo (excepcion maybe??)

    db.session.commit()

    return user

def unblock_user(id: int) -> User:
    user = get_user(id)
    if user is None:
        raise ValueError("No se encontro un usuario con ese ID")
    user.enabled = True
    db.session.commit()

    return user

# funcionalidad para asignar o desasignar un rol a un usuario
def assign_role(id: int, role: str) -> User:
    user = get_user(id)
    if user is None:
        raise ValueError("No se encontro un usuario con ese ID")
    if user.system_admin == False:
        user.role = role
        db.session.commit()
    #else:
        # se tira exception??

    return user

def unassign_role(id: int) -> User:
    user = get_user(id)
    if user is None:
        raise ValueError("No se encontro un usuario con ese ID")
    if user.system_admin == False:
        user.role = None
        db.session.commit()
    #else:
        # se tira exception??

    return user
'''#Implementados en user_operations

# funcionalidad para verificar permisos

def has_permission(user: User, permission_name:str) -> bool:    # pensar en hacer los permisos un Enum
    # verifica que el rol del usuario tenga el permiso especificado
    role = Role.query.get(user.role_id)
    return any(permission.name == permission_name for permission in role.permissions)

"""
#Creacion de un decorator que consulte los permisos para agregarlos a las funciones del CRUD.
#se anota como @permission_required('user_index') (como ejemplo, puede recibir cualquier permiso como param)
def permission_required(permission: str):
    #Decorator para verificar si el usuario tiene el permiso necesario.
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = get_current_user()  # Función que devuelve el usuario autenticado
            if not has_permission(user, permission):
                #abort(403)  # Retorna un error 403 si no tiene el permiso, lo dejo como opcion para el futuro.
                raise PermissionError("No se tiene permiso para realizar esta accion")
            return func(*args, **kwargs)
        return wrapper
    return decorator
"""




# funcionalidad para el seed para crear roles y permisos.
"""
def create_role(**kwargs):
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()
"""#En role_operations
"""
def create_permission(**kwargs):
    permission = Permission(**kwargs)
    db.session.add(permission)
    db.session.commit()
"""#En permission_operations


