from src.model import auth
def run():
    rol_tecnica = auth.create_role(id=1, name='Tecnica')
    rol_ecuestre = auth.create_role(id=2, name='Ecuestre')
    rol_voluntariado = auth.create_role(id=3, name='Voluntariado')
    rol_administracion = auth.create_role(id=4, name='Administracion')
    
    user1 = auth.create_user(alias='Juan', password=123, email='juan@gmail.com', enabled=True, system_admin=True)
    user2 = auth.create_user(alias='Martin', password=123, email='martin@gmail.com', enabled=True, role_id=1)
    user3 = auth.create_user(alias='Sofia', password=123, email='sofia@gmail.com', enabled=True, role_id=2)
    user4 = auth.create_user(alias='Pedro', password=123, email='pedro@gmail.com', enabled=True, role_id=3)


