from src.model.database import db

class CollectionMedium(db.Model):
    __tablename__ = 'collection_mediums'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    
    # relacion 1 a N, un cobro tiene un unico medio de pago y un medio de pago muchos cobros
    collections = db.relationship('Collection', back_populates='medium')

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<MedioPago {self.name}>"
