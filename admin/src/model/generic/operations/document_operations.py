from typing import Optional
from src.model.database import db
from src.model.generic.tables.document import Document
from datetime import datetime
from sqlalchemy.orm  import Query

def create_document(title: str, format: str, is_external: bool, allowed_operations: str, file_address: str, employee_id=None,
                    rider_id=None, type_id: Optional[int] = None, upload_date: datetime = datetime.now()) -> Document:
    document = Document(
        title=title,
        type_id=type_id,
        format=format,
        upload_date=upload_date,
        is_external=is_external,
        allowed_operations=allowed_operations,
        file_address=file_address,
        employee_id=employee_id,
        rider_id=rider_id
    )
    db.session.add(document)
    db.session.commit()
    db.session.expunge(document)
    return document

def list_documents():
    documents = Document.query.all()
    [db.session.expunge(document) for document in documents]
    return documents

def get_document(id: int) -> Document:
    document = Document.query.get(id)
    db.session.expunge(document)
    return document

def update_document(to_update: Document) -> Document:
    document = Document.query.get(to_update.id)
    if document is None:
        raise ValueError("No se encontró un documento con ese ID")
    document.title = to_update.title or document.title
    document.type_id = to_update.type_id or document.type_id
    document.format = to_update.format or document.format
    document.upload_date = to_update.upload_date or document.upload_date
    document.is_external = to_update.is_external if to_update.is_external is not None else document.is_external
    document.allowed_operations = to_update.allowed_operations or document.allowed_operations
    document.file_address = to_update.file_address or document.file_address
    document.employee_id = to_update.employee_id or document.employee_id
    document.rider_id = to_update.rider_id or document.rider_id
    db.session.commit()
    db.session.expunge(document)
    return document

def delete_document(id: int):
    document = Document.query.get(id)
    if document is None:
        raise ValueError("No se encontró un documento con ese ID")
    db.session.delete(document)
    db.session.commit()



# Instrucciones de listado específicas

# Ordena por un atributo específico (título por defecto)
def sorted_by_attribute(documents: Query, attribute: str = "title", ascending: bool = True) -> Query:
    return documents.order_by(getattr(Document, attribute).asc() if ascending else getattr(Document, attribute).desc())

# Búsqueda por título
def search_by_title(documents: Query, title: str = "") -> Query:
    if title:
        return documents.filter(Document.title.ilike(f"%{title}%"))
    return documents

# Búsqueda por tipo de documento
def search_by_type(documents: Query, type_name: str = "") -> Query:
    if type_name:
        return documents.join(DocumentType).filter(DocumentType.name.ilike(f"%{type_name}%"))
    return documents

# Función final que combina los filtros y búsquedas
def get_documents_filtered_list(page: int,
                                limit: int = 25,
                                sort_attr: str = "title",
                                ascending: bool = True,
                                search_title: str = "",
                                search_type: str = "") -> Query:
    # Inicia la consulta con Document
    documents = Document.query
    
    # Aplica los filtros y búsquedas
    documents = search_by_title(documents, search_title)
    documents = search_by_type(documents, search_type)
    
    # Ordena los resultados
    documents = sorted_by_attribute(documents, sort_attr, ascending)
    
    # Pagina los resultados
    document_list = documents.paginate(page=page, per_page=limit, error_out=False)
    
    # Expulsa los objetos de la sesión
    [db.session.expunge(document) for document in document_list.items]
    
    return document_list
