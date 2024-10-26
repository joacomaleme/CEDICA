from src.model.database import db
from src.model.riders.tables.rider_document import RiderDocument

def create_horse_document(rider_id: int, document_id: int) -> RiderDocument:
    rider_document = RiderDocument(rider_id, document_id)
    db.session.add(rider_document)
    db.session.commit()
    db.session.expunge(rider_document)
    return rider_document 

def delete_rider_document(document_id: int):
    rider_document = RiderDocument.query.filter(RiderDocument.document_id == document_id).first()
    if rider_document is None:
        raise ValueError("No se encontró un documento con ese ID")

    db.session.delete(rider_document)
    db.session.commit()