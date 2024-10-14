from src.model.database import db

"""
    Relación entre Riders y Guardians (puede haber varios responsables por jinete)
"""

rider_guardians = db.Table('rider_guardians',
    db.Column('rider_id', db.BigInteger, db.ForeignKey('riders.id'), primary_key=True),
    db.Column('guardian_id', db.BigInteger, db.ForeignKey('guardians.id'), primary_key=True)
)



# class RiderGuardian(db.Model):
#     __tablename__ = 'rider_guardians'

#     id = db.Column(db.BigInteger, primary_key=True)  # Identificador único
#     rider_id = db.Column(db.Integer, db.ForeignKey('riders.id', ondelete="CASCADE"))
#     guardian_id = db.Column(db.BigInteger, db.ForeignKey('guardians.id', ondelete="CASCADE"))


#     # Relaciones
#     rider = db.relationship("Rider", back_populates="guardians", cascade="all, delete-orphan")
#     guardian = db.relationship("Guardian", backref="rider_guardians", cascade="all, delete-orphan")

#     # rider = db.relationship('Rider', back_populates='rider_guardians')
#     # guardian = db.relationship('Guardian', back_populates='rider_guardians')
