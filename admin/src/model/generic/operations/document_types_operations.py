from src.model.database import db
from src.model.generic.tables.document_types import DocumentType

def create_document_type(name):
    document_type = DocumentType(name=name)
    db.session.add(document_type)
    db.session.commit()
    db.session.expunge(document_type)
    return document_type

def get_document_type(document_type_id):
    document_type = DocumentType.query.get(document_type_id)
    db.session.expunge(document_type)
    return document_type

def list_document_type():
    document_types = DocumentType.query.all()
    [db.session.expunge(document_type) for document_type in document_types]
    return document_types

def delete_document_type(document_type_id):
    document_type = DocumentType.query.get(document_type_id)
    if document_type is None:
        raise ValueError("No se encontro un tipo de documento con ese ID")
    db.session.delete(document_type)
    db.session.commit()
