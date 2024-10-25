from typing import List, Optional
from src.model.database import db
from src.model.registers.tables.collection_medium import CollectionMedium


def create_collection_medium(name: str) -> CollectionMedium:
    """ Crea un nuevo medio de pago (MedioPago), lo agrega a la base de datos y retorna el objeto expurgado.  """
    collection_medium = CollectionMedium(name)
    db.session.add(collection_medium)
    db.session.commit()
    db.session.expunge(collection_medium)
    return collection_medium


def list_collection_mediums() -> List[CollectionMedium]:
    """ Lista todos los medios de pago (CollectionMedium) de la base de datos. """
    collection_mediums = CollectionMedium.query.all()
    [db.session.expunge(collection_medium) for collection_medium in collection_mediums]
    return collection_mediums


def get_collection_medium(id: int) -> Optional[CollectionMedium]:
    """ recupera un medio de pago (CollectionMedium) por su id. """
    collection_medium = CollectionMedium.query.get(id)
    if collection_medium:
        db.session.expunge(collection_medium)
    return collection_medium

def get_collection_medium_by_name(name: str) -> Optional[CollectionMedium]:
    """
    Recupera un medio de pago (CollectionMedium) por su nombre.
    Si no se encuentra el nombre, retorna None.

    Parámetros:
    name : str
        El nombre del medio de pago que se desea recuperar.

    Retorna:
    Optional[CollectionMedium]
        El objeto CollectionMedium expurgado si se encuentra, de lo contrario None.
    """
    collection_medium = CollectionMedium.query.filter(CollectionMedium.name == name).first()
    if collection_medium:
        db.session.expunge(collection_medium)
    return collection_medium

def update_collection_medium(to_update: CollectionMedium) -> CollectionMedium:
    """ Actualiza un medio de pago (CollectionMedium) existente con nuevos atributos y guarda los cambios en la base de datos. """
    collection_medium = CollectionMedium.query.get(to_update.id)
    if collection_medium is None:
        raise ValueError("No collection medium found with that ID")
    
    collection_medium.name = to_update.name
    db.session.commit()
    db.session.expunge(collection_medium)
    return collection_medium

def delete_collection_medium(id: int):
    """
        Elimina un medio de pago (CollectionMedium) por su ID.
        Si no se encuentra el registro, lanza una excepción.
    """
    collection_medium = CollectionMedium.query.get(id)
    if collection_medium is None:
        raise ValueError("No collection medium found with that ID")
    db.session.delete(collection_medium)
    db.session.commit()