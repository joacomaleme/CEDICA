from src.model import auth
def run():
    user1 = auth.create_user(alias='Juan', password=123, email='juan@gmail.com', activo='SI', rol="Tecnica")
    user2 = auth.create_user(alias='Martin', password=123, email='martin@gmail.com', activo='SI',rol="Tecnica")
    user3 = auth.create_user(alias='Sofia', password=123, email='sofia@gmail.com', activo='SI', rol="Tecnica")

