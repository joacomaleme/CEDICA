from src.model.database import db

"""
    Tabla de relacion entre los distintos Riders y sus distintos dias de trabajo
"""

class RiderWorkDay(db.Model):
    __tablename__ = 'rider_work_day'

    rider_id = db.Column(db.Integer, db.ForeignKey('riders.id'), primary_key=True)
    work_day_id = db.Column(db.Integer, db.ForeignKey('work_days.id'), primary_key=True)
