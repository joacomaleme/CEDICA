from typing import Optional
from src.model.database import db
from src.model.generic.tables.work_proposal import WorkProposal

def create_work_proposal(name):
    work_proposal = WorkProposal(name=name)
    db.session.add(work_proposal)
    db.session.commit()
    db.session.expunge(work_proposal)
    return work_proposal

def list_work_proposals():
    work_proposals = WorkProposal.query.all()
    [db.session.expunge(wp) for wp in work_proposals]
    return work_proposals


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

def search_name(work_proposal_name: str) -> Optional[WorkProposal]:
    work_proposal = WorkProposal.query.filter_by(name=work_proposal_name).first()
    if work_proposal:
        db.session.expunge(work_proposal)
    return work_proposal