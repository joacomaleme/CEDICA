from src.model.database import db
from src.model.registros.tables.cobro import Cobro
from src.model.registros.tables.medio_pago import MedioPago
from sqlalchemy.orm import Query
from sqlalchemy import desc

from typing import List, Optional
from datetime import datetime

def create_cobro(monto: float, fecha_pago: datetime, observaciones: str, recibe_dinero_id: int, medio_pago_id: int, jinete_y_amazona_id: int) -> Cobro:
    """
    Crea un nuevo cobro (Cobro), lo agrega a la base de datos y retorna el objeto expurgado.

    Parámetros:
    monto : float
        El monto del cobro.
    fecha_pago : datetime
        La fecha en la que se realizó el cobro.
    observaciones : str
        Observaciones adicionales del cobro.
    recibe_dinero_id : int
        El id de la persona que recibe el dinero.
    medio_pago_id : int
        El id del medio de pago utilizado.
    jinete_y_amazona_id : int
        El id del jinete o amazona asociado al cobro.

    Retorna:
    Cobro
        El objeto Cobro recién creado y expurgado.
    """
    cobro = Cobro(monto, fecha_pago, observaciones, recibe_dinero_id, medio_pago_id, jinete_y_amazona_id)
    db.session.add(cobro)
    db.session.commit()
    db.session.expunge(cobro)
    return cobro

def list_cobros() -> List[Cobro]:   
    """
    Lista todos los cobros (Cobro) de la base de datos.
    Retorna una lista vacía si no hay registros.

    Retorna:
    List[Cobro]
        Una lista de objetos Cobro expurgados.
    """
    cobros = Cobro.query.all()
    [db.session.expunge(cobro) for cobro in cobros]
    return cobros

def get_cobro(id: int) -> Optional[Cobro]:
    """
    Recupera un cobro (Cobro) por su ID.
    Si no se encuentra el ID, retorna None.

    Parámetros:
    id : int
        El ID del cobro que se desea recuperar.

    Retorna:
    Cobro
        El objeto Cobro expurgado si se encuentra, de lo contrario None.
    """
    cobro = Cobro.query.get(id)
    if cobro:
        db.session.expunge(cobro)
    return cobro

def update_cobro(to_update: Cobro) -> Cobro:
    """
    Actualiza un cobro (Cobro) existente con nuevos atributos
    y guarda los cambios en la base de datos.

    Parámetros:
    to_update : Cobro
        Una instancia de Cobro con los atributos actualizados.

    Retorna:
    Cobro
        El objeto Cobro actualizado y expurgado.

    Lanza:
    ValueError
        Si no se encuentra un Cobro con el ID proporcionado.
    """
    cobro = Cobro.query.get(to_update.id)
    if cobro is None:
        raise ValueError("No se encontró un cobro con ese ID")
    
    cobro.monto = to_update.monto or cobro.monto
    cobro.fecha_pago = to_update.fecha_pago or cobro.fecha_pago
    cobro.observaciones = to_update.observaciones or cobro.observaciones
    cobro.recibe_dinero_id = to_update.recibe_dinero_id
    cobro.medio_pago_id = to_update.medio_pago_id
    cobro.jinete_y_amazona_id = to_update.jinete_y_amazona_id

    db.session.commit()
    db.session.expunge(cobro)
    return cobro

def delete_cobro(id: int):
    """
    Elimina un cobro (Cobro) por su ID.
    Si no se encuentra el registro, lanza una excepción.

    Parámetros:
    id : int
        El ID del cobro que se desea eliminar.

    Lanza:
    ValueError
        Si no se encuentra un Cobro con el ID proporcionado.
    """
    cobro = Cobro.query.get(id)
    if cobro is None:
        raise ValueError("No se encontró un cobro con ese ID")

    db.session.delete(cobro)
    db.session.commit()

def filter_fecha_pago(cobros: Query, fecha_inicio: datetime, fecha_fin: datetime) -> Query:
    """
    Filtra los cobros (Cobro) entre un rango de fechas.

    Parámetros:
    cobros : Query
        Query de la tabla de cobros a filtrar.
    fecha_inicio : datetime
        Fecha de inicio del rango.
    fecha_fin : datetime
        Fecha de fin del rango.

    Retorna:
    Query
        Query filtrado con los cobros dentro del rango de fechas.
    """
    return cobros.filter(db.and_((Cobro.fecha_pago > fecha_inicio), (Cobro.fecha_pago < fecha_fin)))

def filter_medio_pago(cobros: Query, medios_pago: List[MedioPago]) -> Query:
    """
    Filtra los cobros (Cobro) por medio de pago (MedioPago).

    Parámetros:
    cobros : Query
        Query de la tabla de cobros a filtrar.
    medios_pago : List[MedioPago]
        Lista de medios de pago por los cuales se desea filtrar.

    Retorna:
    Query
        Query filtrado con los cobros que coinciden con los medios de pago especificados.
    """
    return cobros.filter(Cobro.medio_pago.id.in_(medio_pago.id for medio_pago in medios_pago))

def search_by_name_recibe_dinero(cobros: Query, name: str) -> Query:
    """
    Filtra los cobros (Cobro) por el nombre de la persona que recibe el dinero.

    Parámetros:
    cobros : Query
        Query de la tabla de cobros a filtrar.
    name : str
        El nombre de la persona que recibe el dinero.

    Retorna:
    Query
        Query filtrado con los cobros donde el nombre de la persona coincide.
    """
    return cobros.filter(Employee.name.ilike(f"%{name}%"))

def search_by_surname_recibe_dinero(cobros: Query, surname: str) -> Query:
    """
    Filtra los cobros (Cobro) por el apellido de la persona que recibe el dinero.

    Parámetros:
    cobros : Query
        Query de la tabla de cobros a filtrar.
    surname : str
        El apellido de la persona que recibe el dinero.

    Retorna:
    Query
        Query filtrado con los cobros donde el apellido de la persona coincide.
    """
    return cobros.filter(Employee.surname.ilike(f"%{surname}%"))

def sorted_by_fecha_pago(cobros: Query, ascending: bool = True) -> Query:
    """
    Ordena los cobros (Cobro) por fecha.

    Parámetros:
    cobros : Query
        Query de la tabla de cobros a ordenar.
    ascending : bool, opcional
        Define si el orden es ascendente (True) o descendente (False). Por defecto, es ascendente.

    Retorna:
    Query
        Query ordenado por la fecha de los cobros.
    """
    if ascending:
        return cobros.order_by(Cobro.fecha_pago)
    else:
        return cobros.order_by(desc(Cobro.fecha_pago))

def get_filtered_list(page: int, limit: int = 25, medios_pago: List[MedioPago] = [], ascending: bool = True,
                      fecha_inicio: datetime = None, fecha_fin: datetime = None, name: str = "", surname: str = "") -> List[Cobro]:
    """
    Obtiene una lista paginada de cobros (Cobro) filtrada por fecha, medios de pago, y nombre o apellido
    de la persona que recibe el dinero, y ordenada por fecha.

    Parámetros:
    page : int
        Número de página para la paginación.
    limit : int, opcional
        Número máximo de resultados por página. Por defecto es 25.
    medios_pago : List[MedioPago], opcional
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
    List[Cobro]
        Lista paginada de cobros filtrados y ordenados.
    """
    if medios_pago == []:
        medios_pago = MedioPago.query.all()

    cobro_list = filter_fecha_pago(Cobro.query, fecha_inicio, fecha_fin)
    cobro_list = filter_medio_pago(cobro_list, medios_pago)
    cobro_list = search_by_name_recibe_dinero(cobro_list, name)
    cobro_list = search_by_surname_recibe_dinero(cobro_list, surname)
    cobro_list = sorted_by_fecha_pago(cobro_list, ascending)

    cobros = cobro_list.paginate(page=page, per_page=limit)
    [db.session.expunge(cobro) for cobro in cobros]
    return cobros
