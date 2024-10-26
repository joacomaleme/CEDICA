from src.model.database import db
from src.model.horses.tables.horse_document import HorseDocument

def create_horse_document(horse_id: int, document_id: int) -> HorseDocument:
    horse_document = HorseDocument(horse_id, document_id)
    db.session.add(horse_document)
    db.session.commit()
    db.session.expunge(horse_document)
    return horse_document

def delete_horse_document(id: int):
    horse_document = HorseDocument.query.filter(HorseDocument.document_id == id).first()
    if horse_document is None:
        raise ValueError("No se encontro un documento con ese ID")

    db.session.delete(horse_document)
    db.session.commit()
