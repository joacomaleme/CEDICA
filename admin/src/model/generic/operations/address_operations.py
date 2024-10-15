from typing import Optional
from src.model.database import db
from src.model.generic.tables.address import Address

# Operaciones del CRUD de las direcciones.

def create_address(street: str, number: str, apartment: Optional[str] = None):
    address = Address(street=street, number=number, apartment=apartment)
    db.session.add(address)
    db.session.commit()
    db.session.expunge(address)
    return address

def get_addres(id: int):
    address = Address.query.get(id)
    if address:
        db.session.expunge(address)
    return address # si no encuentra nada devuelve None

def update_address(to_update: Address) -> Address:
    address = Address.query.get(to_update.id)
    if address is None:
        raise ValueError("No se encontro un address con ese ID") 
    
    address.street = to_update.street or address.street
    address.number = to_update.number or address.number
    address.apartment = to_update.apartment or address.apartment
    db.session.commit()
    db.session.expunge(address)
    return address