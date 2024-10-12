from flask import session
from flask import abort
# para la administracion de permisos y para hacer el decorator
from functools import wraps # un decorator que hace que se mantengan los metadatos de la funcion cuando esta siendo decorada, util para debuggear.

#Creacion de un decorator que consulte los permisos para agregarlos a las funciones del CRUD.
#se anota como @permission_required('user_index') (como ejemplo. Puede recibir cualquier permiso como param)
def login_required():
    #Decorator para verificar si el usuario tiene el permiso necesario.
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_email = session.get("user")
            if not user_email:
                return abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator

