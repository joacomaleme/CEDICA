from src.model.database import db
from src.model.registers.tables.payment import Payment
from src.model.registers.tables.payment_type import PaymentType
from sqlalchemy.orm import Query
from sqlalchemy import desc

from typing import List, Optional
from datetime import datetime

def create_payment(amount: float, date: datetime, description: str, payment_type_id: int, beneficiary_id: Optional[int] = None) -> Payment:
    """
    Crea un nuevo pago (Pago), lo agrega a la base de datos y retorna el objeto expurgado.

    Parámetros:
    beneficiario : int
        El id del beneficiario del pago.
    monto : float
        El monto del pago.
    fecha_pago : datetime
        La fecha en la que se realizó el pago.
    descripcion : str
        Descripción del pago.
    tipo_pago : int
        El id del tipo de pago asociado.

    Retorna:
    Pago
        El objeto Pago recién creado y expurgado.
    """
    payment = Payment(amount, date, description, payment_type_id, beneficiary_id)
    db.session.add(payment)
    db.session.commit()
    db.session.expunge(payment)
    return payment

def list_payments() -> List[Payment]:   
    """
    Lista todos los pagos (Pago) de la base de datos. 
    Retorna una lista vacía si no hay registros.

    Retorna:
    List[Pago]
        Una lista de objetos Pago expurgados.
    """
    payments = Payment.query.all()
    [db.session.expunge(payment) for payment in payments]
    return payments

def get_payment(id: int) -> Optional[Payment]:
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
    payment = Payment.query.get(id)
    if payment:
        db.session.expunge(payment)
    return payment

def update_payment(to_update: Payment) -> Payment:
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
    payment = Payment.query.get(to_update.id)
    if payment is None:
        raise ValueError("No se encontró un pago con ese ID")
    
    payment.beneficiary_id = to_update.beneficiary_id
    payment.amount = to_update.amount or payment.amount
    payment.date = to_update.date or payment.date
    payment.description = to_update.description or payment.description
    payment.payment_type_id = to_update.payment_type_id

    db.session.commit()
    db.session.expunge(payment)
    return payment

def delete_payment(id: int):
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
    payment = Payment.query.get(id)
    if payment is None:
        raise ValueError("No se encontró un pago con ese ID")

    db.session.delete(payment)
    db.session.commit()

def filter_date(payments: Query, start_date: datetime, end_date: datetime) -> Query:
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
    return payments.filter(db.and_((Payment.date > start_date), (Payment.date < end_date)))

def filter_payment_type(payments: Query, payment_types: List[PaymentType]) -> Query:
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
    return payments.filter(Payment.payment_type_id.in_(payment_type.id for payment_type in payment_types))

def sorted_by_date(payments: Query, ascending: bool = True) -> Query:
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
        return payments.order_by(Payment.date)
    else:
        return payments.order_by(desc(Payment.date))

def get_filtered_list(page: int, limit: int = 25, payment_types: List[PaymentType] = [],
                       ascending: bool = True, start_date: datetime = None, end_date: datetime = None) -> List[Payment]:        # hacer las datetimes Optional[]
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
        Una lista que contiene una Lista paginada de pagos filtrados y ordenados, y también un integer de la cantidad de páginas que entraban en el Query
        pre-paginación.
    """
    if payment_types == []:
        payment_types = PaymentType.query.all()

    payment_list = sorted_by_date(
                filter_payment_type(
                filter_date(Payment.query, start_date, end_date), payment_types), ascending)
    paginated_list = payment_list.paginate(page=page, per_page=limit, error_out=False).items

    [db.session.expunge(payment) for payment in paginated_list]
    return [paginated_list, ((payment_list.count()-1)//limit)+1]
