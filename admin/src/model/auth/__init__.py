from src.model.database import db
from src.model.auth.user import User

def list_users():
    users = User.query.all()

    return users

def create_user(**kwargs):
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user
