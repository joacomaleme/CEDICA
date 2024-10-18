from src.model.database import db

class RiderDocument(db.Model):
    __tablename__ = 'rider_documents'
    rider_id = db.Column(db.BigInteger, db.ForeignKey('riders.id'), primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), primary_key=True)
    rider = db.relationship("Rider", back_populates="rider_documents")
    document = db.relationship("Document", backref="rider_documents")

    def __init__(self, rider_id: int, document_id: int):
        self.rider_id = rider_id 
        self.document_id = document_id 
