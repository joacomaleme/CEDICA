from src.model.database import db
class Province(db.Model):  # Tabla para Provincias
    __tablename__ = 'provinces'

    id = db.Column(db.BigInteger, primary_key=True)  # Identificador único
    name = db.Column(db.String(100), nullable=False, unique=True)  # Nombre de la provincia

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'<Province {self.name}>'
