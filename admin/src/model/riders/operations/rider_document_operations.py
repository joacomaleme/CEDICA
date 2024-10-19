from src.model.database import db
from src.model.riders.tables.rider_document import RiderDocument

def create_horse_document(rider_id: int, document_id: int) -> RiderDocument:
    rider_document = RiderDocument(rider_id, document_id)
    db.session.add(rider_document)
    db.session.commit()
    db.session.expunge(rider_document)
    return rider_document 
