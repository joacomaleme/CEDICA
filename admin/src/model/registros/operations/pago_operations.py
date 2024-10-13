from src.model.database import db
from src.model.registros.tables.pago import Pago
from src.model.registros.tables.tipo_pago import TipoPago
from sqlalchemy.orm import Query
from sqlalchemy import desc

from typing import List, Optional
from datetime import datetime

def create_pago(beneficiario, monto: float, fecha_pago: datetime, descripcion: str, tipo_pago: TipoPago) -> Pago:
    """
    Crea un nuevo pago (Pago), lo agrega a la base de datos y retorna el objeto expurgado.

    Parámetros:
    beneficiario : EMPLEADO
        El nombre del beneficiario del pago.
    monto : float
        El monto del pago.
    fecha_pago : datetime
        La fecha en la que se realizó el pago.
    descripcion : str
        Descripción del pago.
    tipo_pago : TipoPago
        El tipo de pago asociado.

    Retorna:
    Pago
        El objeto Pago recién creado y expurgado.
    """
    pago = Pago(beneficiario, monto, fecha_pago, descripcion, tipo_pago)
    db.session.add(pago)
    db.session.commit()
    db.session.expunge(pago)
    return pago

def list_pagos() -> List[Pago]:   
    """
    Lista todos los pagos (Pago) de la base de datos. 
    Retorna una lista vacía si no hay registros.

    Retorna:
    List[Pago]
        Una lista de objetos Pago expurgados.
    """
    pagos = Pago.query.all()
    [db.session.expunge(pago) for pago in pagos]
    return pagos

def get_pago(id: int) -> Optional[Pago]:
    """
    Recupera un pago (Pago) por su ID.
    Si no se encuentra el ID, retorna None.

    Parámetros:
    id : int
        El ID del pago que se desea recuperar.

    Retorna:
    Pago
        El objeto Pago expurgado si se encuentra, de lo contrario None.
    """
    pago = Pago.query.get(id)
    if pago:
        db.session.expunge(pago)
    return pago

def update_pago(to_update: Pago) -> Pago:
    """
    Actualiza un pago (Pago) existente con nuevos atributos
    y guarda los cambios en la base de datos.

    Parámetros:
    to_update : Pago
        Una instancia de Pago con los atributos actualizados.

    Retorna:
    Pago
        El objeto Pago actualizado y expurgado.

    Lanza:
    ValueError
        Si no se encuentra un Pago con el ID proporcionado.
    """
    pago = Pago.query.get(to_update.id)
    if pago is None:
        raise ValueError("No se encontró un pago con ese ID")
    
    pago.beneficiario = to_update.beneficiario
    pago.monto = to_update.monto or pago.monto
    pago.fecha_pago = to_update.fecha_pago or pago.fecha_pago
    pago.descripcion = to_update.descripcion or pago.descripcion
    pago.tipo_pago = to_update.tipo_pago

    db.session.commit()
    db.session.expunge(pago)
    return pago

def delete_pago(id: int):
    """
    Elimina un pago (Pago) por su ID.
    Si no se encuentra el registro, lanza una excepción.

    Parámetros:
    id : int
        El ID del pago que se desea eliminar.

    Lanza:
    ValueError
        Si no se encuentra un Pago con el ID proporcionado.
    """
    pago = Pago.query.get(id)
    if pago is None:
        raise ValueError("No se encontró un pago con ese ID")

    db.session.delete(pago)
    db.session.commit()

def filter_fecha_pago(pagos: Query, fecha_inicio: datetime, fecha_fin: datetime) -> Query:
    """
    Filtra los pagos (Pago) entre un rango de fechas.

    Parámetros:
    pagos : Query
        Query de la tabla de pagos a filtrar.
    fecha_inicio : datetime
        Fecha de inicio del rango.
    fecha_fin : datetime
        Fecha de fin del rango.

    Retorna:
    Query
        Query filtrado con los pagos dentro del rango de fechas.
    """
    return pagos.filter(db.and_((Pago.fecha_pago > fecha_inicio), (Pago.fecha_pago < fecha_fin)))

def filter_tipo_pago(pagos: Query, tipos_pago: List[TipoPago]) -> Query:
    """
    Filtra los pagos (Pago) por tipo de pago (TipoPago).

    Parámetros:
    pagos : Query
        Query de la tabla de pagos a filtrar.
    tipos_pago : List[TipoPago]
        Lista de tipos de pago por los cuales se desea filtrar.

    Retorna:
    Query
        Query filtrado con los pagos que coinciden con los tipos de pago especificados.
    """
    return pagos.filter(Pago.tipo_pago.id.in_(tipo_pago.id for tipo_pago in tipos_pago))

def sorted_by_fecha_pago(pagos: Query, ascending: bool = True) -> Query:
    """
    Ordena los pagos (Pago) por fecha.

    Parámetros:
    pagos : Query
        Query de la tabla de pagos a ordenar.
    ascending : bool, opcional
        Define si el orden es ascendente (True) o descendente (False). Por defecto, es ascendente.

    Retorna:
    Query
        Query ordenado por la fecha de los pagos.
    """
    if ascending:
        return pagos.order_by(Pago.fecha_pago)
    else:
        return pagos.order_by(desc(Pago.fecha_pago))

def get_filtered_list(page: int, limit: int = 25, tipos_pago: List[TipoPago] = [],
                       ascending: bool = True, fecha_inicio: datetime = None, fecha_fin: datetime = None) -> List[Pago]:
    """
    Obtiene una lista paginada de pagos (Pago) filtrada por fecha y tipos de pago,
    y ordenada por fecha.

    Parámetros:
    page : int
        Número de página para la paginación.
    limit : int, opcional
        Número máximo de resultados por página. Por defecto es 25.
    tipos_pago : List[TipoPago], opcional
        Lista de tipos de pago para filtrar. Si no se proporciona, se usarán todos los tipos de pago.
    ascending : bool, opcional
        Define si el orden es ascendente (True) o descendente (False). Por defecto, es ascendente.
    fecha_inicio : datetime, opcional
        Fecha de inicio para el filtro de rango de fechas.
    fecha_fin : datetime, opcional
        Fecha de fin para el filtro de rango de fechas.

    Retorna:
    List[Pago]
        Lista paginada de pagos filtrados y ordenados.
    """
    if tipos_pago == []:
        tipos_pago = TipoPago.query.all()

    pago_list = sorted_by_fecha_pago(
                filter_tipo_pago(
                filter_fecha_pago(Pago.query, fecha_inicio, fecha_fin), tipos_pago), ascending)\
                .paginate(page=page, per_page=limit, error_out=False)

    [db.session.expunge(pago) for pago in pago_list.items]
    return pago_list