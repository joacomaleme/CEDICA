from src.model.auth.operations.user_operations import has_permission

def is_authenticated(session):
  return session.get("user") is not None

def is_permitted(session, permission:str) -> bool:
  return is_authenticated(session) and has_permission(session.get("user"), permission)

def is_self(session, email:str) -> bool:
  return session.get("user") == email