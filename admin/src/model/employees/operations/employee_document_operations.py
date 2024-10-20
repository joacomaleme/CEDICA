from src.model.database import db
from src.model.employees.tables.employee_document import EmployeeDocument

def create_employee_document(employee_id: int, document_id: int) -> EmployeeDocument:
    employee_document = EmployeeDocument(employee_id, document_id)
    db.session.add(employee_document)
    db.session.commit()
    db.session.expunge(employee_document)
    return employee_document

def delete_employee_document(document_id: int):
    employee_document = EmployeeDocument.query.filter(EmployeeDocument.document_id == document_id).first()
    if employee_document is None:
        raise ValueError("No se encontró un documento con ese ID")

    db.session.delete(employee_document)
    db.session.commit()