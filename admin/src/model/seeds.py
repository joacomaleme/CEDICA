from src.model import auth
def run():
    # Creado de permisos
    user_index = auth.create_permission(id=1, name='user_index')
    user_new = auth.create_permission(id=2, name='user_new')
    user_destroy = auth.create_permission(id=3, name='user_destroy')
    user_update = auth.create_permission(id=4, name='user_update')
    user_show = auth.create_permission(id=5, name='user_show')

    # Creado de roles
    rol_tecnica = auth.create_role(id=1, name='Tecnica')
    rol_ecuestre = auth.create_role(id=2, name='Ecuestre')
    rol_voluntariado = auth.create_role(id=3, name='Voluntariado')
    rol_administracion = auth.create_role(id=4, name='Administracion')

    # Asignacion de permisos a roles
    auth.assign_permission(rol_tecnica, [user_index, user_show])
    auth.assign_permission(rol_ecuestre, [user_index, user_show])
    auth.assign_permission(rol_voluntariado, user_index)
    auth.assign_permission(rol_administracion, [user_index, user_new, user_update, user_show])

    #Rol de system_admin? Suena más lindo que el boolean. No es lo que hicieron en el ejemplo, pero el ejemplo no es ley.
    
    user1 = auth.create_user(alias='Juan', password=123, email='juan@gmail.com', enabled=True, system_admin=True)
    user2 = auth.create_user(alias='Martin', password=123, email='martin@gmail.com', enabled=True, role_id=1)
    user3 = auth.create_user(alias='Sofia', password=123, email='sofia@gmail.com', enabled=True, role_id=2)
    user4 = auth.create_user(alias='Pedro', password=123, email='pedro@gmail.com', enabled=True, role_id=3)
