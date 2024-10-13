from src.model.database import db
from src.model.employees.tables.document import Document

def create_document(title: str, type: str, file_address: str, employee_id: int) -> Document:
    document = Document(title, type, file_address, employee_id)
    db.session.add(document)
    db.session.commit()
    db.session.expunge(document)
    return document

def get_document_by_file_address(file_address: str):
    document = Document.query.filter(Document.file_address == file_address).first()
    if document:
        db.session.expunge(document)
    return document # si no encuentra nada devuelve None