from src.model.database import db
from src.model.generic.tables.address import Address

# Operaciones del CRUD de las direcciones.

def create_address(street, number, apartment=None):
    address = Address(street=street, number=number, apartment=apartment)
    db.session.add(address)
    db.session.commit()
    db.session.expunge(address)
    return address
