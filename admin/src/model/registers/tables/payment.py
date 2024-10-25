from src.model.database import db
from datetime import datetime
from typing import Optional

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.BigInteger, primary_key=True)
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime)
    description = db.Column(db.String(1024))

    # Relacion con tipo de pago
    payment_type_id = db.Column(db.BigInteger, db.ForeignKey('payment_types.id'))
    payment_type = db.relationship('PaymentType', back_populates='payments')

    # Relacion con beneficiario
    beneficiary_id = db.Column(db.BigInteger, db.ForeignKey('employees.id', ondelete='CASCADE'))
    beneficiary = db.relationship('Employee', back_populates='payments', passive_deletes=True)

    def __init__(self, amount: float, date: datetime, description: str, payment_type_id: int, beneficiary_id: Optional[int] = None):
        self.amount = amount 
        self.date = date
        self.description = description
        self.payment_type_id = payment_type_id
        self.beneficiary_id = beneficiary_id

    def __repr__(self):
        return f"<Payment {self.id}>"
