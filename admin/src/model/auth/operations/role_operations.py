from src.model.database import db
from ..tables.role import Role
from ..tables.permission import Permission
from typing import List, Union
from copy import deepcopy

def create_role(name:str) -> Role:
    role = Role(name)
    db.session.add(role)
    db.session.commit()
    
    return deepcopy(role)


def assign_permission(role: Role, permissions: Union[List[Permission], Permission]):
    """Asigna uno o más permisos a un rol determinado.
    Args:
        role (Role): Una copia profunda de un rol existente.
        permissions (list[Permission] or Permission): Lista de permisos o un solo permiso a asignar.
    """
    # Reconsulta el rol real en la base de datos usando el ID del rol recibido.
    real_role = Role.query.filter_by(id=role.id).first()    # ESTO EXPLOTA

    if not real_role:
        raise ValueError(f"Role with id {role.id} not found in the database")

    # Asigna los permisos.
    if isinstance(permissions, list):
        real_role.permissions.extend(permissions)  # Agregar múltiples permisos
    else:
        real_role.permissions.append(permissions)  # Agregar un único permiso

    # Añadir el rol actualizado a la sesión y confirmar los cambios.
    db.session.add(real_role)
    db.session.commit()

