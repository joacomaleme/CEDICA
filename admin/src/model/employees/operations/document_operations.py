from src.model.database import db
from src.model.employees.tables.document import Document

def create_profession(titulo: str, tipo: str, archivo: str, employee_id: int) -> Document:
    document = Document(titulo, tipo, archivo, employee_id)
    db.session.add(document)
    db.session.commit()
    db.session.expunge(document)
    return document