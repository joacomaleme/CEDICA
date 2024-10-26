from src.model.auth.operations.user_operations import has_permission

def is_authenticated(session):
  #Retorna si hay una sesión iniciada para este usuario
  return session.get("user") is not None

def is_permitted(session, permission:str) -> bool:
  #Retora si hay una sesión iniciada para este usuario, y si el mismo tiene el permiso específico determinado por la string "permission"
  return is_authenticated(session) and has_permission(session.get("user"), permission)

def is_self(session, email:str) -> bool:
  #En base a un mail y la sesión, retorna si el mail corresponde a la sesión específica.
  return session.get("user") == email