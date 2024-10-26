from flask import session
from flask import abort
# para la administracion de permisos y para hacer el decorator
from functools import wraps # un decorator que hace que se mantengan los metadatos de la funcion cuando esta siendo decorada, util para debuggear.


def login_required():
    '''
    Decorator para hacer el login un prerequsito, retorna un abort(401) si no hay una sesión iniciada para este usuario, sino deja proseguir
    a la función decorada
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_email = session.get("user")
            if not user_email:
                return abort(401)
            return func(*args, **kwargs)
        return wrapper
    return decorator

