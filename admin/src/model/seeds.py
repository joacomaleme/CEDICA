from src.model.auth.operations import permission_operations as permissions
from src.model.auth.operations import role_operations as roles
from src.model.auth.operations import user_operations as users
from src.model import auth

def run():
    # Creado de permisos
    user_index = permissions.create_permission(name='user_index')
    user_new = permissions.create_permission(name='user_new')
    user_destroy = permissions.create_permission(name='user_destroy')
    user_update = permissions.create_permission(name='user_update')
    user_show = permissions.create_permission(name='user_show')

    # Creado de roles
    rol_tecnica = roles.create_role(name='Tecnica')
    rol_ecuestre = roles.create_role(name='Ecuestre')
    rol_voluntariado = roles.create_role(name='Voluntariado')
    rol_administracion = roles.create_role(name='Administracion')

    # Asignacion de permisos a roles
    roles.assign_permission(rol_tecnica, [user_index, user_show])
    roles.assign_permission(rol_ecuestre, [user_index, user_show])
    roles.assign_permission(rol_voluntariado, user_index)
    roles.assign_permission(rol_administracion, [user_index, user_new, user_update, user_show])

    #Rol de system_admin? Suena más lindo que el boolean. No es lo que hicieron en el ejemplo, pero el ejemplo no es ley.
    
    user1 = users.create_user(alias='Juan', password=123, email='juan@gmail.com', enabled=True, system_admin=True)
    user2 = users.create_user(alias='Martin', password=123, email='martin@gmail.com', enabled=True, role_id=1)
    user3 = users.create_user(alias='Sofia', password=123, email='sofia@gmail.com', enabled=True, role_id=2)
    user4 = users.create_user(alias='Pedro', password=123, email='pedro@gmail.com', enabled=True, role_id=3)
