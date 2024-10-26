from src.model.database import db

"""
    Esta tabla debe tener todos los dias de la semana
"""

class WorkDay(db.Model):
    __tablename__ = 'work_days'

    id = db.Column(db.Integer, primary_key=True)
    day_name = db.Column(db.String(50), nullable=False, unique=True)  # Lunes, Martes, etc.

    riders = db.relationship('Rider', secondary='rider_work_day', back_populates='work_days')

    def __init__(self, day_name):
        self.day_name = day_name
