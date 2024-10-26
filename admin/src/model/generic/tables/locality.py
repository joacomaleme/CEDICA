from src.model.database import db
class Locality(db.Model):  # Tabla para Localidades
    __tablename__ = 'localities'

    id = db.Column(db.BigInteger, primary_key=True)  # Identificador único
    name = db.Column(db.String(100), nullable=False, unique=True)  # Nombre de la localidad
    
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'<Locality {self.name}>'
