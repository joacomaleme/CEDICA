from src.model.database import db

"""
    Relación entre Riders y Guardians (puede haber varios responsables por jinete)
"""

class RiderGuardian(db.Model):
    __tablename__ = 'rider_guardians'

    rider_id = db.Column(db.BigInteger, db.ForeignKey('riders.id'), primary_key=True)
    guardian_id = db.Column(db.BigInteger, db.ForeignKey('guardians.id'), primary_key=True)

    # Relaciones
    rider = db.relationship('Rider', back_populates='rider_guardians')
    guardian = db.relationship('Guardian', back_populates='rider_guardians')
