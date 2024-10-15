from src.model.database import db

class Horse(db.Model):
    __tablename__ = 'horses'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(8), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, name, gender, breed, age, owner_id=None, active=True):
        self.name = name
        self.gender = gender
        self.breed = breed
        self.age = age
        self.owner_id = owner_id
        self.active = active
