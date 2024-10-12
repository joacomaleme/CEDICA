from src.model.database import db
from src.model.employees.tables.job_position import JobPosition

def create_job_position(name: str) -> JobPosition:
    job_position = JobPosition(name)
    db.session.add(job_position)
    db.session.commit()
    db.session.expunge(job_position)
    return job_position