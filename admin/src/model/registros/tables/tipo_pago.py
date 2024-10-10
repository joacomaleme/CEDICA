from src.model.database import db

class TipoPago(db.Model):
    __tablename__ = 'tipospago'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    
    # relacion 1 a N, un pago tiene un unico tipo y un tipo muchos pagos
    pagos = db.relationship('Pago', back_populates='tipo_pago')

    def __init__(self, name:str):
        self.name = name

    def __repr__(self):
        return f"<TipoPago {self.name}>"
