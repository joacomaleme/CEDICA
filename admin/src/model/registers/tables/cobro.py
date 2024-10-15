from src.model.database import db
from datetime import datetime

class Cobro(db.Model):
    __tablename__ = 'cobros'

    id = db.Column(db.BigInteger, primary_key=True)
    monto = db.Column(db.Float, nullable=False)
    fecha_pago = db.Column(db.DateTime, nullable=False)
    observaciones = db.Column(db.String(255), default="")
    medio_pago_id = db.Column(db.BigInteger, db.ForeignKey('mediospago.id'))
    recibe_dinero_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    jinete_y_amazona_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))

    medio_pago = db.relationship('MedioPago', back_populates='cobros')
    # recibe_dinero = db.relationship('User', back_populates='cobros', foreign_keys=[recibe_dinero_id])     # CAMBIAR A EMPLEADO
    # jinete_y_amazona = db.relationship('User', back_populates='cobros1', foreign_keys=[jinete_y_amazona_id])  # CAMBIAR A J&A Y A COBROS SIN EL 1

    def __init__(self, monto: float, fecha_pago: datetime, observaciones: str, recibe_dinero_id: int, medio_pago_id: int, jinete_y_amazona_id: int):
        self.monto = monto
        self.fecha_pago = fecha_pago
        self.observaciones = observaciones
        self.recibe_dinero_id = recibe_dinero_id
        self.medio_pago_id = medio_pago_id
        self.jinete_y_amazona_id = jinete_y_amazona_id

    def __repr__(self):
        return f"<Cobro {self.id}>"