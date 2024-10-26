from src.model.auth.tables.user import User
from src.model.auth.tables.role import Role
from src.model.auth.operations.user_operations import has_permission
# para la administracion de permisos y para hacer el decorator
from functools import wraps # un decorator que hace que se mantengan los metadatos de la funcion cuando esta siendo decorada, util para debuggear.



#Creacion de un decorator que consulte los permisos para agregarlos a las funciones del CRUD.
#se anota como @permission_required('user_index') (como ejemplo. Puede recibir cualquier permiso como param)
def permission_required(permission: str, user_email: str):
    #Decorator para verificar si el usuario tiene el permiso necesario.
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not has_permission(user_email, permission):
                #abort(403)  # Retorna un error 403 si no tiene el permiso, lo dejo como opcion para el futuro.
                raise PermissionError("No se tiene permiso para realizar esta accion")
            return func(*args, **kwargs)
        return wrapper
    return decorator
