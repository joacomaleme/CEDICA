from typing import List, Optional
from src.model.database import db
from src.model.registros.tables.tipo_pago import TipoPago

def create_tipo_pago(name: str) -> TipoPago:
    """
    Crea un nuevo tipo de pago (TipoPago), lo agrega a la base de datos
    y retorna el objeto expurgado.

    Parámetros:
    name : str
        El nombre del tipo de pago que se desea crear.

    Retorna:
    TipoPago
        El objeto TipoPago recién creado y expurgado.
    """
    tipo_pago = TipoPago(name)
    db.session.add(tipo_pago)
    db.session.commit()
    db.session.expunge(tipo_pago)
    return tipo_pago

def list_tipos_pago() -> List[TipoPago]:
    """
    Recupera todos los tipos de pago (TipoPago) de la base de datos.
    Si no se encuentran registros, retorna una lista vacía.

    Retorna:
    List[TipoPago]
        Una lista de objetos TipoPago expurgados.
    """
    tipos_pago = TipoPago.query.all()
    [db.session.expunge(tipo_pago) for tipo_pago in tipos_pago]
    return tipos_pago

def get_tipo_pago(id: int) -> Optional[TipoPago]:
    """
    Recupera un tipo de pago (TipoPago) por su ID.
    Si no se encuentra el ID, retorna None.

    Parámetros:
    id : int
        El ID del tipo de pago que se desea recuperar.

    Retorna:
    Optional[TipoPago]
        El objeto TipoPago expurgado si se encuentra, de lo contrario None.
    """
    tipo_pago = TipoPago.query.get(id)
    if tipo_pago:
        db.session.expunge(tipo_pago)
    return tipo_pago

def update_pago(to_update: TipoPago) -> TipoPago:
    """
    Actualiza un tipo de pago (TipoPago) existente con nuevos atributos
    y guarda los cambios en la base de datos.

    Parámetros:
    to_update : TipoPago
        Una instancia de TipoPago con los atributos actualizados.

    Retorna:
    TipoPago
        El objeto TipoPago actualizado y expurgado.

    Lanza:
    ValueError
        Si no se encuentra un TipoPago con el ID proporcionado.
    """
    tipo_pago = TipoPago.query.get(to_update.id)
    if tipo_pago is None:
        raise ValueError("No se encontró un tipo de pago con ese ID")
    
    tipo_pago.name = to_update.name

    db.session.commit()
    db.session.expunge(tipo_pago)
    return tipo_pago

def delete_tipo_pago(id: int):
    """
    Elimina un tipo de pago (TipoPago) por su ID.
    Si no se encuentra el registro, lanza una excepción.

    Parámetros:
    id : int
        El ID del tipo de pago que se desea eliminar.

    Lanza:
    ValueError
        Si no se encuentra un TipoPago con el ID proporcionado.
    """
    tipo_pago = TipoPago.query.get(id)
    if tipo_pago is None:
        raise ValueError("No se encontró un tipo de pago con ese ID")

    db.session.delete(tipo_pago)
    db.session.commit()
