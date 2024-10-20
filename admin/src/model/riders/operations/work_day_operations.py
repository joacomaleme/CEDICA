from src.model.database import db
from src.model.riders.tables.work_day import WorkDay

def create_work_day(day):
    work_day = WorkDay(day_name=day)
    db.session.add(work_day)
    db.session.commit()
    db.session.expunge(work_day)
    return work_day

def list_work_days():
    work_days = WorkDay.query.all()
    [db.session.expunge(work_day) for work_day in work_days]
    return work_days

def get_work_day(work_day_id):
    work_day = WorkDay.query.get(work_day_id)
    db.session.expunge(work_day)
    return work_day

def delete_work_day(work_day_id):
    work_day = WorkDay.query.get(work_day_id)
    if work_day is None:
        raise ValueError("No se encontro un dia de trabajo con ese ID")
    db.session.delete(work_day)
    db.session.commit()
