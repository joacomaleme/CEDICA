from src.model.database import db

class HorseDocument(db.Model):
    __tablename__ = 'horse_documents'
    horse_id = db.Column(db.BigInteger, db.ForeignKey('horses.id'), primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), primary_key=True)
    horse = db.relationship("Horse", back_populates="horse_documents")
    document = db.relationship("Document", backref="horse_documents")

    def __init__(self, horse_id: int, document_id: int):
        self.horse_id = horse_id
        self.document_id = document_id
