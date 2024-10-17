from typing import List, Optional
from src.model.database import db
from src.model.registros.tables.medio_pago import MedioPago

def create_medio_pago(name: str) -> MedioPago:
    """
    Crea un nuevo medio de pago (MedioPago), lo agrega a la base de datos y retorna el objeto expurgado.

    Parámetros:
    name : str
        El nombre del medio de pago.

    Retorna:
    MedioPago
        El objeto MedioPago recién creado y expurgado.
    """
    medio_pago = MedioPago(name)
    db.session.add(medio_pago)
    db.session.commit()
    db.session.expunge(medio_pago)
    return medio_pago

def list_medios_pago() -> List[MedioPago]:
    """
    Lista todos los medios de pago (MedioPago) de la base de datos.
    Retorna una lista vacía si no hay registros.

    Retorna:
    List[MedioPago]
        Una lista de objetos MedioPago expurgados.
    """
    medios_pago = MedioPago.query.all()
    [db.session.expunge(medio_pago) for medio_pago in medios_pago]
    return medios_pago

def get_medio_pago(id: int) -> Optional[MedioPago]:
    """
    Recupera un medio de pago (MedioPago) por su ID.
    Si no se encuentra el ID, retorna None.

    Parámetros:
    id : int
        El ID del medio de pago que se desea recuperar.

    Retorna:
    MedioPago
        El objeto MedioPago expurgado si se encuentra, de lo contrario None.
    """
    medio_pago = MedioPago.query.get(id)
    if medio_pago:
        db.session.expunge(medio_pago)
    return medio_pago

def update_pago(to_update: MedioPago) -> MedioPago:
    """
    Actualiza un medio de pago (MedioPago) existente con nuevos atributos
    y guarda los cambios en la base de datos.

    Parámetros:
    to_update : MedioPago
        Una instancia de MedioPago con los atributos actualizados.

    Retorna:
    MedioPago
        El objeto MedioPago actualizado y expurgado.

    Lanza:
    ValueError
        Si no se encuentra un MedioPago con el ID proporcionado.
    """
    medio_pago = MedioPago.query.get(to_update.id)
    if medio_pago is None:
        raise ValueError("No se encontró un medio de pago con ese ID")
    
    medio_pago.name = to_update.name

    db.session.commit()
    db.session.expunge(medio_pago)
    return medio_pago

def delete_medio_pago(id: int):
    """
    Elimina un medio de pago (MedioPago) por su ID.
    Si no se encuentra el registro, lanza una excepción.

    Parámetros:
    id : int
        El ID del medio de pago que se desea eliminar.

    Lanza:
    ValueError
        Si no se encuentra un MedioPago con el ID proporcionado.
    """
    medio_pago = MedioPago.query.get(id)
    if medio_pago is None:
        raise ValueError("No se encontró un medio de pago con ese ID")

    db.session.delete(medio_pago)
    db.session.commit()
