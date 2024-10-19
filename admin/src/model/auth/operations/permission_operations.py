from src.model.database import db
from src.model.auth.tables.permission import Permission


def create_permission(name:str) -> Permission:
    '''
        Recibe un nombre (string), y crea un permiso en la Base de Datos con ese nombre, 
        luego retorna el objeto que representa a ese permiso, pero desconectado de la BD
    '''
    permission = Permission(name)
    db.session.add(permission)
    db.session.commit()
    db.session.expunge(permission)
    return permission
