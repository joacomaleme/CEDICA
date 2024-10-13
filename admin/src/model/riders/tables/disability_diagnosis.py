from src.model.database import db

"""
    Tabla que representa los posibles diagnosticos, en la consigna se nombran:
    ECNE, Lesión post-traumática;  Mielomeningocele, Esclerosis Múltiple, Escoliosis Leve, Secuelas de ACV; Discapacidad Intelectual; Trastorno del Espectro Autista; Trastorno del Aprendizaje; Trastorno del Aprendizaje; Trastorno por Déficit de Atención/Hiperactividad; Trastorno de la Comunicación; Trastorno de Ansiedad; Síndrome de Down; Retraso Madurativo; Psicosis; Trastorno de Conducta; Trastornos del ánimo y afectivos; Trastorno Alimentario; OTRO
"""

class DisabilityDiagnosis(db.Model):  # Tabla para Diagnósticos de Discapacidad
    __tablename__ = 'disability_diagnoses'

    id = db.Column(db.BigInteger, primary_key=True)  # Identificador único
    diagnosis = db.Column(db.String(255), nullable=False, unique=True)  # Descripción del diagnóstico
    extra_comment = db.Column(db.String(255)) # En caso de que sea "OTRO" y/o se quiera aclarar algo en especifico.

    def __repr__(self):
        return f'<DisabilityDiagnosis {self.diagnosis}>'
