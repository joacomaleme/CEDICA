from src.model.database import db
from src.model.generic.tables.sede import Sede
from src.model.horses.tables.horse_document import HorseDocument
from datetime import datetime

class Horse(db.Model):
    __tablename__ = 'horses'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth = db.Column(db.Date, nullable=False)
    sex = db.Column(db.Boolean, nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    coat = db.Column(db.String(64), nullable=False)

    #   boolean para saber si el caballo es donado o si se compro
    is_donated = db.Column(db.Boolean, nullable=False, default=False)

    inserted_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    # relacion con la tabla de sede
    sede_id = db.Column(db.BigInteger, db.ForeignKey('sedes.id'), nullable=False)
    sede = db.relationship('Sede', backref='horses', foreign_keys=[sede_id], lazy='joined')

    active = db.Column(db.Boolean, default=True)

    # relacion con employees (entrenadores y conductores)
    employees = db.relationship('Employee', secondary='horses_employees', back_populates='horses', lazy='joined')

    # relacion con la tabla de WorkProposal (la actividad asignada al caballo)
    activity_id = db.Column(db.BigInteger, db.ForeignKey('work_proposals.id'), nullable=False)
    activity = db.relationship('WorkProposal', backref='horses', foreign_keys=[activity_id], lazy='joined')


    horse_documents = db.relationship("HorseDocument", back_populates="horse", cascade="all, delete-orphan")
    documents = db.relationship("Document", secondary="horse_documents", viewonly=True)

    def __init__(self, name, birth, sex, breed, coat, is_donated, sede_id, active, activity_id):
        self.name = name
        self.birth = birth
        self.sex = sex
        self.breed = breed
        self.coat = coat
        self.is_donated = is_donated
        self.sede_id = sede_id
        self.active = active
        self.activity_id = activity_id
