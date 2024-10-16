from src.model.database import db
from src.model.registers.tables.collection import Collection
from src.model.registers.tables.collection_medium import CollectionMedium
from src.model.employees.tables.employee import Employee
from sqlalchemy.orm import Query
from sqlalchemy import desc

from typing import List, Optional
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


def filter_by_date(collections: Query, start_date: Optional[datetime], end_date: Optional[datetime]) -> Query:
    """ Filtra los cobros (Collection) entre un rango de fechas. """
    return collections.filter(db.and_((Collection.date > start_date), (Collection.date  < end_date)))

def filter_by_medium(collections: Query, collection_mediums: List[CollectionMedium]) -> Query:
    """ Filtra los cobros (Collection) por medio de pago (MedioPago). """
    return collections.filter(Collection.collection_medium_id.in_(medium.id for medium in collection_mediums))

def search_by_name_of_received_by(collections: Query, name: str) -> Query:
    """ Filtra los cobros (Collection) por el nombre de la persona que recibe el dinero. """
    return collections.filter(Employee.name.ilike(f"%{name}%"))

def search_by_surname_of_received_by(collections: Query, surname: str) -> Query:
    """ Filtra los cobros (Collection) por el apellido de la persona que recibe el dinero. """
    return collections.filter(Employee.surname.ilike(f"%{surname}%"))

def sorted_by_date(collections: Query, ascending: bool = True) -> Query:
    """ Ordena los cobros (Collection) por fecha. """
    if ascending:
        return collections.order_by(Collection.payment_date)
    else:
        return collections.order_by(desc(Collection.payment_date))


def get_filtered_list(page: int, limit: int = 25, collection_mediums: List[CollectionMedium] = [], ascending: bool = True,
                      start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, name: str = "", surname: str = "") -> List[Collection]:
    """
        Obtiene una lista paginada de cobros (Collection) filtrada por fecha, medios de pago, y nombre o apellido
        de la persona que recibe el dinero, y ordenada por fecha.

        Parámetros:
        page : int
            Número de página para la paginación.
        limit : int, opcional
            Número máximo de resultados por página. Por defecto es 25.
        medios_pago : List[CollectionMedium], opcional
            Lista de medios de pago para filtrar. Si no se proporciona, se usarán todos los medios de pago.
        ascending : bool, opcional
            Define si el orden es ascendente (True) o descendente (False). Por defecto, es ascendente.
        fecha_inicio : datetime, opcional
            Fecha de inicio para el filtro de rango de fechas.
        fecha_fin : datetime, opcional
            Fecha de fin para el filtro de rango de fechas.
        name : str, opcional
            Nombre de la persona que recibe el dinero.
        surname : str, opcional
            Apellido de la persona que recibe el dinero.

        Retorna:
        List[Collection]
            Lista paginada de cobros filtrados y ordenados.
    """
    if collection_mediums == []:
        collection_mediums = CollectionMedium.query.all()

    collection_list = filter_by_date(Collection.query, start_date, end_date)
    collection_list = filter_by_medium(collection_list, collection_mediums)
    collection_list = search_by_name_of_received_by(collection_list, name)
    collection_list = search_by_surname_of_received_by(collection_list, surname)
    collection_list = sorted_by_date(collection_list, ascending)

    collections = collection_list.paginate(page=page, per_page=limit)
    [db.session.expunge(collection) for collection in collections]
    return collections
