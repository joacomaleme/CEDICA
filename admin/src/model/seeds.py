from src.model.auth.operations import permission_operations as permissions
from src.model.auth.operations import role_operations as roles
from src.model.auth.operations import user_operations as users

from src.model.registros.operations import pago_operations as pagos
from src.model.registros.operations import tipo_pago_operations as tipos_pago

from src.model.registros.operations import cobro_operations as cobros
from src.model.registros.operations import medio_pago_operations as medios_pago
from src.model import auth

from datetime import datetime

def run():
    ############
    # Usuarios #
    ############

    # Creado de roles
    rol_tecnica = roles.create_role(name='Tecnica')
    rol_ecuestre = roles.create_role(name='Ecuestre')
    rol_voluntariado = roles.create_role(name='Voluntariado')
    rol_administracion = roles.create_role(name='Administracion')

    # Creado de permisos
    user_index = permissions.create_permission(name='user_index')
    user_new = permissions.create_permission(name='user_new')
    user_destroy = permissions.create_permission(name='user_destroy')
    user_update = permissions.create_permission(name='user_update')
    user_show = permissions.create_permission(name='user_show')

    # Asignacion de permisos a roles
    roles.assign_permission(rol_tecnica, [user_index, user_show])
    roles.assign_permission(rol_ecuestre, [user_index, user_show])
    roles.assign_permission(rol_voluntariado, user_index)
    roles.assign_permission(rol_administracion, [user_index, user_new, user_update, user_show])

    #Rol de system_admin? Suena más lindo que el boolean. No es lo que hicieron en el ejemplo, pero el ejemplo no es ley.
    
    user1 = users.create_user(alias='Juan', password="123", email='juan@gmail.com', enabled=True, system_admin=True)
    user2 = users.create_user(alias='Martin', password="123", email='martin@gmail.com', enabled=True, role_id=1)
    user3 = users.create_user(alias='Sofia', password="123", email='sofia@gmail.com', enabled=False, role_id=2)
    user4 = users.create_user(alias='Pedro', password="123", email='pedro@gmail.com', enabled=True, role_id=3)

    #####################
    # REGISTRO DE PAGOS #
    #####################

    # Creado de permisos
    pago_index = permissions.create_permission(name='pago_index')
    pago_new = permissions.create_permission(name='pago_new')
    pago_destroy = permissions.create_permission(name='pago_destroy')
    pago_update = permissions.create_permission(name='pago_update')
    pago_show = permissions.create_permission(name='pago_show')

    # Asignacion de permisos a roles
    roles.assign_permission(rol_administracion, [pago_index, pago_new, pago_destroy, pago_update, pago_show])

    # Creado de tipos de pago
    tipos_pago.create_tipo_pago("Honorarios")
    tipos_pago.create_tipo_pago("Proveedor")
    tipos_pago.create_tipo_pago("Gastos Varios")

    # Creado de pagos
    pagos.create_pago(beneficiario_id=1, monto=5000, fecha_pago=datetime(2024, 9, 10), descripcion="Pago realizado", tipo_pago_id=1)
    pagos.create_pago(beneficiario_id=1, monto=7200, fecha_pago=datetime.now(), descripcion="El pago fue exitoso", tipo_pago_id=3)
    pagos.create_pago(beneficiario_id=2, monto=1300, fecha_pago=datetime(2024, 9, 15), descripcion="Un muy buen pago", tipo_pago_id=1)
    pagos.create_pago(beneficiario_id=4, monto=10200.50, fecha_pago=datetime(1999, 2, 20), descripcion="Pago de un proveedor", tipo_pago_id=2)

    ######################
    # REGISTRO DE COBROS #
    ######################

    # Creado de permisos
    cobro_index = permissions.create_permission(name='cobro_index')
    cobro_new = permissions.create_permission(name='cobro_new')
    cobro_destroy = permissions.create_permission(name='cobro_destroy')
    cobro_update = permissions.create_permission(name='cobro_update')
    cobro_show = permissions.create_permission(name='cobro_show')

    # Asignacion de permisos a roles
    roles.assign_permission(rol_administracion, [cobro_index, cobro_new, cobro_destroy, cobro_update, cobro_show])
    roles.assign_permission(rol_tecnica, [cobro_index, cobro_show])

    # Creado de medios de pago
    medios_pago.create_medio_pago("Efectivo")
    medios_pago.create_medio_pago("Tarjeta de Crédito")
    medios_pago.create_medio_pago("Tarjeta de Débito")

    # Creado de cobros
    cobros.create_cobro(monto=200, fecha_pago=datetime.now(), observaciones="Un buen cobro", recibe_dinero_id=1, medio_pago_id=1, jinete_y_amazona_id=2)
    cobros.create_cobro(monto=700, fecha_pago=datetime(2024, 8, 10), observaciones="Gran cobro", recibe_dinero_id=2, medio_pago_id=3, jinete_y_amazona_id=1)
    cobros.create_cobro(monto=150, fecha_pago=datetime(2024, 1, 20), observaciones="No solucinado", recibe_dinero_id=2, medio_pago_id=2, jinete_y_amazona_id=3)
    cobros.create_cobro(monto=1200, fecha_pago=datetime(1998, 9, 15), observaciones="El último", recibe_dinero_id=4, medio_pago_id=2, jinete_y_amazona_id=1)
