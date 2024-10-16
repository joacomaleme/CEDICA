from typing import List, Optional
from src.model.database import db
from src.model.registers.tables.payment_type import PaymentType

def create_payment_type(name: str) -> PaymentType:
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
    payment_type = PaymentType(name)
    db.session.add(payment_type)
    db.session.commit()
    db.session.expunge(payment_type)
    return payment_type

def list_payment_types() -> List[PaymentType]:
    """
    Recupera todos los tipos de pago (TipoPago) de la base de datos.
    Si no se encuentran registros, retorna una lista vacía.

    Retorna:
    List[TipoPago]
        Una lista de objetos TipoPago expurgados.
    """
    payment_types = PaymentType.query.all()
    [db.session.expunge(payment_type) for payment_type in payment_types]
    return payment_types 

def get_payment_type(id: int) -> Optional[PaymentType]:
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
    payment_type = PaymentType.query.get(id)
    if payment_type:
        db.session.expunge(payment_type)
    return payment_type

def get_payment_type_by_name(name: str) -> Optional[PaymentType]:
    """
    Recupera un tipo de pago (TipoPago) por su nombre.
    Si no se encuentra el nombre, retorna None.

    Parámetros:
    name : str
        El nombre del tipo de pago que se desea recuperar.

    Retorna:
    Optional[TipoPago]
        El objeto TipoPago expurgado si se encuentra, de lo contrario None.
    """
    payment_type = PaymentType.query.filter(PaymentType.name == name).first()
    if payment_type:
        db.session.expunge(payment_type)
    return payment_type

def update_payment(to_update: PaymentType) -> PaymentType:
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
    payment_type = PaymentType.query.get(to_update.id)
    if payment_type is None:
        raise ValueError("No se encontró un tipo de pago con ese ID")
    
    payment_type.name = to_update.name

    db.session.commit()
    db.session.expunge(payment_type)
    return payment_type

def delete_payment_type(id: int):
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
    payment_type= PaymentType.query.get(id)
    if payment_type is None:
        raise ValueError("No se encontró un tipo de pago con ese ID")

    db.session.delete(payment_type)
    db.session.commit()
