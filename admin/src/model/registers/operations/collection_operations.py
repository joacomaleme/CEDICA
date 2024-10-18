from src.model.database import db
from src.model.registers.tables.collection import Collection
from src.model.registers.tables.collection_medium import CollectionMedium
from src.model.employees.tables.employee import Employee
from sqlalchemy.orm import Query
from sqlalchemy import desc

from typing import List, Optional, Tuple
from datetime import datetime


def create_collection(amount: float, date: datetime, observations: str, received_by_id: int, medium_id: int, paid_by_id: int) -> Collection:
    """Crea un nuevo cobro (Collection), lo agrega a la base de datos y retorna el objeto expurgado."""
    collection = Collection(amount, date, observations, medium_id, received_by_id, paid_by_id)
    db.session.add(collection)
    db.session.commit()
    db.session.expunge(collection)
    return collection


def list_collections() -> List[Collection]:
    """Lista todos los cobros (Collection) de la base de datos. Retorna una lista vacía si no hay registros."""
    collections = Collection.query.all()
    [db.session.expunge(collection) for collection in collections]
    return collections


def get_collection(id: int) -> Optional[Collection]:
    """Recupera un cobro (Collection) por su ID. Si no se encuentra el ID, retorna None."""
    collection = Collection.query.get(id)
    if collection:
        db.session.expunge(collection)
    return collection


def update_collection(to_update: Collection) -> Collection:
    """Actualiza un cobro (Collection) existente con nuevos atributos y guarda los cambios en la base de datos."""
    collection = Collection.query.get(to_update.id)
    if collection is None:
        raise ValueError("No se encontró un cobro con ese ID")
    collection.amount = to_update.amount or collection.amount
    collection.date = to_update.date or collection.date
    collection.observations = to_update.observations or collection.observations
    collection.received_by_id = to_update.received_by_id
    collection.medium_id = to_update.medium_id
    collection.paid_by_id = to_update.paid_by_id
    db.session.commit()
    db.session.expunge(collection)
    return collection


def delete_collection(id: int):
    """Elimina un cobro (Collection) por su ID. Si no se encuentra el registro, lanza una excepción."""
    collection = Collection.query.get(id)
    if collection is None:
        raise ValueError("No se encontró un cobro con ese ID")
    db.session.delete(collection)
    db.session.commit()

from sqlalchemy.orm import aliased

def filter_by_date(collections: Query, start_date: Optional[datetime], end_date: Optional[datetime]) -> Query:
    """ Filtra los cobros (Collection) entre un rango de fechas. """
    if not start_date:
        start_date = datetime.min
    
    if not end_date:
        end_date = datetime.now()

    return collections.filter(db.and_(Collection.date >= start_date, Collection.date <= end_date))


def filter_by_medium(collections: Query, collection_mediums: List[CollectionMedium]) -> Query:
    """ Filtra los cobros (Collection) por medio de pago (MedioPago). """
    return collections.filter(Collection.medium_id.in_(medium.id for medium in collection_mediums))


def search_by_name_of_received_by(collections: Query, name: str) -> Query:
    """ Filtra los cobros (Collection) por el nombre de la persona que recibe el dinero. """
    # Alias for Employee to avoid duplicate table names in case of multiple joins
    employee_alias = aliased(Employee)
    collections = collections.join(employee_alias, Collection.received_by_id == employee_alias.id)
    return collections.filter(employee_alias.name.ilike(f"%{name}%"))


def search_by_surname_of_received_by(collections: Query, surname: str) -> Query:
    """ Filtra los cobros (Collection) por el apellido de la persona que recibe el dinero. """
    # Alias for Employee to avoid duplicate table names in case of multiple joins
    employee_alias = aliased(Employee)
    collections = collections.join(employee_alias, Collection.received_by_id == employee_alias.id)
    return collections.filter(employee_alias.surname.ilike(f"%{surname}%"))

def search_by_attribute(collections: Query, search_attr: str = "name", search_value: str = "") -> Query:
    employee_alias = aliased(Employee)
    collections = collections.join(employee_alias, Collection.received_by_id == employee_alias.id)

    match search_attr:
        case "name":
            return collections.filter(employee_alias.name.ilike(f"%{search_value}%"))
        case "surname":
            return collections.filter(employee_alias.surname.ilike(f"%{search_value}%"))
        case _:
            return collections.filter(employee_alias.name.ilike(f"%{search_value}%"))

def sorted_by_date(collections: Query, ascending: bool = True) -> Query:
    """ Ordena los cobros (Collection) por fecha. """
    if ascending:
        return collections.order_by(Collection.date)
    else:
        return collections.order_by(desc(Collection.date))


def get_filtered_list(page: int, limit: int = 25, collection_mediums: List[CollectionMedium] = [], ascending: bool = True,
                      start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, search_attr: str = "name", search_value: str = "") -> Tuple[List[Collection], int]:
    """
        Obtiene una lista paginada de cobros (Collection) filtrada por fecha, medios de pago, y nombre o apellido
        de la persona que recibe el dinero, y ordenada por fecha.
    """
    if not collection_mediums:
        collection_mediums = CollectionMedium.query.all()

    # Start with a base query
    collection_query = Collection.query

    collection_query = filter_by_date(collection_query, start_date, end_date)
    collection_query = filter_by_medium(collection_query, collection_mediums)
    collection_query = search_by_attribute(collection_query, search_attr, search_value)
    collection_query = sorted_by_date(collection_query, ascending)

    paginated_list = collection_query.paginate(page=page, per_page=limit, error_out=False).items

    [db.session.expunge(collection) for collection in paginated_list]

    total_pages = (collection_query.count() - 1) // limit + 1
    return (paginated_list, total_pages)