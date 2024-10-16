from src.model.database import db

"""
    Relación entre Riders y Guardians (puede haber varios responsables por jinete)
"""

class RiderGuardian(db.Model):
    __tablename__ = 'rider_guardians'
    id = db.Column(db.BigInteger, primary_key=True)  # Identificador único
    rider_id = db.Column(db.Integer, db.ForeignKey('riders.id', ondelete="CASCADE"))
    guardian_id = db.Column(db.BigInteger, db.ForeignKey('guardians.id', ondelete="CASCADE"))

    relationship = db.Column(db.String(20), nullable=False)   # Relación con el jinete (Padre, Madre, Tutor/a)

    __table_args__ = (
        db.UniqueConstraint('rider_id', 'guardian_id', name='_rider_guardian_uc'),  # Ensures unique combination of rider and guardian
    )
