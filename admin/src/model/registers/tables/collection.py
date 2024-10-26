from src.model.database import db
from datetime import datetime

class Collection(db.Model):
    __tablename__ = 'collections'

    id = db.Column(db.BigInteger, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    observations = db.Column(db.String(255), default="")

    # Relacion con el medio de pago, y los actores involucrados en la transaccion
    medium_id = db.Column(db.BigInteger, db.ForeignKey('collection_mediums.id'))
    medium = db.relationship('CollectionMedium', back_populates='collections', foreign_keys=[medium_id])

    paid_by_id = db.Column(db.BigInteger, db.ForeignKey('riders.id', ondelete='CASCADE'))
    paid_by = db.relationship('Rider', 
                            foreign_keys=[paid_by_id],
                            back_populates='paid_collections',
                            passive_deletes=True)

    received_by_id = db.Column(db.BigInteger, db.ForeignKey('employees.id', ondelete='CASCADE'))
    received_by = db.relationship('Employee', 
                               foreign_keys=[received_by_id],
                               back_populates='received_collections',
                               passive_deletes=True)

    def __init__(self, amount: float, date: datetime, observations: str, medium_id: int, received_by_id: int, paid_by_id: int):
        self.amount = amount
        self.date = date
        self.observations = observations
        self.medium_id = medium_id
        self.received_by_id = received_by_id
        self.paid_by_id = paid_by_id

    def __repr__(self):
        return f"<Cobro {self.id}>"
