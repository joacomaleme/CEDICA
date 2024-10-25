from src.model.database import db
from src.model.employees.tables.job_position import JobPosition

def create_job_position(name: str) -> JobPosition:
    job_position = JobPosition(name)
    db.session.add(job_position)
    db.session.commit()
    db.session.expunge(job_position)
    return job_position

def list_job_positions():
    job_positions = JobPosition.query.all()
    [db.session.expunge(job_position) for job_position in job_positions]
    return job_positions

def search_name(job_position_name: str) -> JobPosition:
    job_position = JobPosition.query.filter_by(name=job_position_name).first()
    if job_position is None:
        raise ValueError("No se encontro un job_position con ese ID")
    
    db.session.expunge(job_position)
    return job_position