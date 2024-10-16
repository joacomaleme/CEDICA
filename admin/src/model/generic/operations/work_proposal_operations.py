from src.model.database import db
from src.model.generic.tables.work_proposal import WorkProposal

def create_work_proposal(name):
    work_proposal = WorkProposal(name=name)
    db.session.add(work_proposal)
    db.session.commit()
    db.session.expunge(work_proposal)
    return work_proposal

def get_work_proposal(work_proposal_id):
    work_proposal = WorkProposal.query.get(work_proposal_id)
    db.session.expunge(work_proposal)
    return work_proposal

def delete_work_proposal(work_proposal_id):
    work_proposal = WorkProposal.query.get(work_proposal_id)
    if work_proposal is None:
        raise ValueError("No se encontro una propuesta de trabajo con ese ID")
    db.session.delete(work_proposal)
    db.session.commit()
