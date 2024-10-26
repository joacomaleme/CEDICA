from src.model.database import db

class PaymentType(db.Model):
    __tablename__ = 'payment_types'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)   #Honorarios | proveedor | gastos varios
    
    # relacion 1 a N, un pago tiene un unico tipo y un tipo muchos pagos
    payments = db.relationship('Payment', back_populates='payment_type')

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<PaymentType {self.name}>"
