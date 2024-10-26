from src.model.database import db
from src.model.riders.tables.disability_diagnosis import DisabilityDiagnosis

def create_disability_diagnosis(diagnosis):
    disability_diagnosis = DisabilityDiagnosis(diagnosis=diagnosis)
    db.session.add(disability_diagnosis)
    db.session.commit()
    db.session.expunge(disability_diagnosis)
    return disability_diagnosis

def list_disability_diagnosis():
    disabilities_diagnosis = DisabilityDiagnosis.query.all()
    [db.session.expunge(disability_diagnosis) for disability_diagnosis in disabilities_diagnosis]
    return disabilities_diagnosis

def get_disability_diagnosis(disability_diagnosis_id):
    disability_diagnosis = DisabilityDiagnosis.query.get(disability_diagnosis_id)
    db.session.expunge(disability_diagnosis)
    return disability_diagnosis

def get_disability_diagnosis_by_diagnosis(disability_diagnosis_name: str):
    disability_diagnosis = DisabilityDiagnosis.query.filter(DisabilityDiagnosis.diagnosis == disability_diagnosis_name).first()
    if disability_diagnosis:
        db.session.expunge(disability_diagnosis)
    return disability_diagnosis

def delete_disability_diagnosis(disability_diagnosis_id):
    disability_diagnosis = DisabilityDiagnosis.query.get(disability_diagnosis_id)
    if disability_diagnosis is None:
        raise ValueError("No se encontro un diagnosis de discapacidad con ese ID")
    db.session.delete(disability_diagnosis)
    db.session.commit()
