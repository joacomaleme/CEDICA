from src.model.database import db

class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.BigInteger, primary_key=True)
    street = db.Column(db.String(255), nullable=False)  # Calle
    number = db.Column(db.String(10), nullable=False)  # Número
    apartment = db.Column(db.String(10))  # Departamento, opcional


    def __init__(self, street, number, apartment=None):
        self.street = street
        self.number = number
        self.apartment = apartment
