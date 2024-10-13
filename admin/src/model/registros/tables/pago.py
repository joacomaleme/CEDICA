from src.model.database import db
from datetime import datetime

class Pago(db.Model):
    __tablename__ = 'pagos'

    id = db.Column(db.BigInteger, primary_key=True)
    monto = db.Column(db.Float)
    fecha_pago = db.Column(db.DateTime)
    descripcion = db.Column(db.String(255))
    tipo_pago_id = db.Column(db.BigInteger, db.ForeignKey('tipospago.id'))
    beneficiario_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))

    tipo_pago = db.relationship('TipoPago', back_populates='pagos')
    beneficiario = db.relationship('User', back_populates='pagos')

    def __init__(self, beneficiario: 'User', monto: float, fecha_pago: datetime, descripcion: str, tipo_pago: 'TipoPago'):
        self.beneficiario = beneficiario
        self.monto = monto
        self.fecha_pago = fecha_pago
        self.descripcion = descripcion
        self.tipo_pago = tipo_pago

    def __repr__(self):
        return f"<Pago {self.id}>"
