from src.model.database import db
from datetime import datetime

class Pago(db.Model):
    __tablename__ = 'pagos'

    id = db.Column(db.BigInteger, primary_key=True)
    monto = db.Column(db.Float, nullable=False)
    fecha_pago = db.Column(db.DateTime, nullable=False)
    descripcion = db.Column(db.String(255), default="")
    tipo_pago_id = db.Column(db.BigInteger, db.ForeignKey('tipospago.id'))
    beneficiario_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))

    tipo_pago = db.relationship('TipoPago', back_populates='pagos')
    beneficiario = db.relationship('User', back_populates='pagos')

    def __init__(self, beneficiario_id: int, monto: float, fecha_pago: datetime, descripcion: str, tipo_pago_id: int):
        self.beneficiario_id = beneficiario_id
        self.monto = monto
        self.fecha_pago = fecha_pago
        self.descripcion = descripcion
        self.tipo_pago_id = tipo_pago_id

    def __repr__(self):
        return f"<Pago {self.id}>"
