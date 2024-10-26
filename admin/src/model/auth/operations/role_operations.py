from src.model.database import db
from src.model.auth.tables.role import Role
from src.model.auth.tables.permission import Permission
from typing import List, Union


def create_role(name:str) -> Role:
    '''
        Recibe un nombre (string), y crea un rol en la Base de Datos con ese nombre, 
        luego retorna el objeto que representa a ese rol, pero desconectado de la BD
    '''
    role = Role(name)
    db.session.add(role)
    db.session.commit()
    db.session.expunge(role)
    return role #Explota incluso sin esto

def list_roles() -> List[Role]:
    '''
    Retorna una lista con las representaciones en objeto de todos los roles registrados en la BD
    desconectados de la misma.
    '''
    roles = Role.query.all()
    [db.session.expunge(role) for role in roles]
    return roles # puede devolver una lista vacia

def search_name(role_name:str) -> Role:
    '''
    Dado un nombre (string) retorna un objeto tipo Role que tenga ese nombre, desconectado de la BD, o None, si no encuentra ninguno. 
    '''
    role = Role.query.filter_by(name=role_name).first()
    if role:
        db.session.expunge(role)
    return role

def assign_permission(role: Role, permissions: Union[List[Permission], Permission]):
    """Asigna uno o más permisos a un rol determinado.
    Args:
        role (Role): Una copia profunda de un rol existente.
        permissions (list[Permission] or Permission): Lista de permisos o un solo permiso a asignar.
    """
    # Reconsulta el rol real en la base de datos usando el ID del rol recibido.
    real_role = Role.query.filter_by(id=role.id).first()

    if not real_role:
        raise ValueError(f"Role with id {role.id} not found in the database")

    # Asigna los permisos.
    if isinstance(permissions, list):
        real_role.permissions.extend(permissions)  # Agregar múltiples permisos
    else:
        real_role.permissions.append(permissions)  # Agregar un único permiso

    # Añadir el rol actualizado a la sesión y confirmar los cambios.
    
    db.session.commit()

