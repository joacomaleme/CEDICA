from src.model.auth.operations import permission_operations as permissions
from src.model.auth.operations import role_operations as roles
from src.model.auth.operations import user_operations as users
from src.model.employees.operations import employee_operations as employees
from src.model.employees.operations import job_position_operations as job_positions
from src.model.employees.operations import profession_operations as professions
from src.model.registers.operations import payment_operations as pagos
from src.model.registers.operations import payment_type_operations as tipos_pago
from src.model import auth

from datetime import datetime

def run():
    ############
    # Usuarios #
    ############

    # Creado de roles
    system_admin = roles.create_role(name='system_admin')
    rol_tecnica = roles.create_role(name='Tecnica')
    rol_ecuestre = roles.create_role(name='Ecuestre')
    rol_voluntariado = roles.create_role(name='Voluntariado')
    rol_administracion = roles.create_role(name='Administracion')

    # Creado de permisos para usuarios
    user_index = permissions.create_permission(name='user_index')
    user_new = permissions.create_permission(name='user_new')
    user_destroy = permissions.create_permission(name='user_destroy')
    user_update = permissions.create_permission(name='user_update')
    user_show = permissions.create_permission(name='user_show')

    # permisos para empleados
    employee_index = permissions.create_permission(name='employee_index')
    employee_new = permissions.create_permission(name='employee_new') 
    employee_destroy = permissions.create_permission(name='employee_destroy')
    employee_show = permissions.create_permission(name='employee_show')
    employee_update = permissions.create_permission(name='employee_update')

    # permisos para pagos
    payment_index = permissions.create_permission(name='payment_index')
    payment_show = permissions.create_permission(name='payment_show')
    payment_update = permissions.create_permission(name='payment_update')
    payment_create = permissions.create_permission(name='payment_create')
    payment_destroy = permissions.create_permission(name='payment_destroy')

    # Asignacion de permisos a roles de usuario
    roles.assign_permission(system_admin, [user_index, user_new, user_update, user_show, user_destroy, employee_index, employee_new, employee_destroy, employee_show, employee_update, payment_index, payment_show, payment_update, payment_create, payment_destroy])
    roles.assign_permission(rol_tecnica, [user_index, user_show])
    roles.assign_permission(rol_ecuestre, [user_index, user_show])
    roles.assign_permission(rol_voluntariado, user_index)
    roles.assign_permission(rol_administracion, [user_index, user_new, user_update, user_show, employee_index, employee_new, employee_destroy, employee_show, employee_update, payment_index, payment_show, payment_update, payment_create, payment_destroy])

    user1 = users.create_user(alias='Juan', password='123a', email='juan@gmail.com', enabled=True)
    user2 = users.create_user(alias='Martin', password='123a', email='martin@gmail.com', enabled=True, role_id=1)
    user3 = users.create_user(alias='Sofia', password='123a', email='sofia@gmail.com', enabled=True, role_id=2)
    user4 = users.create_user(alias='Pedro', password='123a', email='pedro@gmail.com', enabled=True, role_id=3)


    #############
    # Empleados #
    #############

    # Creado de profesiones
    professions.create_profession("Médico/a")
    professions.create_profession("Docente")
    professions.create_profession("Psicólogo/a")
    professions.create_profession("Otro")

    # Creado de posiciones
    job_positions.create_job_position("Terapeuta")
    job_positions.create_job_position("Domador")
    job_positions.create_job_position("Profesor de Equitación")
    job_positions.create_job_position("Otro")

    # Creado de empleados
    employees.create_employee(name='María', surname='Gómez', dni=45678901, address='Calle Falsa 123', email='maria.gomez@example.com', locality='Buenos Aires', phone='1122334455', profession_id=1, job_position_id=2, emergency_contact_name='Juan Gómez', emergency_contact_phone='1198765432', obra_social='OSDE', affiliate_number='ABC123456', is_volunteer=False, enabled=True)
    employees.create_employee(name='Carlos', surname='Pérez', dni=23456789, address='Av. Libertador 456', email='carlos.perez@example.com', locality='Córdoba', phone='1167891234', profession_id=2, job_position_id=3, emergency_contact_name='Ana Pérez', emergency_contact_phone='1145678901', obra_social='Swiss Medical', affiliate_number='XYZ789012', is_volunteer=False, enabled=True)
    employees.create_employee(name='Lucía', surname='Fernández', dni=34567890, address='Calle Las Rosas 789', email='lucia.fernandez@example.com', locality='Rosario', phone='1156781234', profession_id=3, job_position_id=4, emergency_contact_name='Clara Fernández', emergency_contact_phone='1178901234', obra_social='Galeno', affiliate_number='LMN456789', is_volunteer=True, enabled=True)
    employees.create_employee(name='Javier', surname='López', dni=56789012, address='Pasaje Mitre 12', email='javier.lopez@example.com', locality='Mendoza', phone='1123456789', profession_id=4, job_position_id=1, emergency_contact_name='Sofía López', emergency_contact_phone='1124567890', obra_social='OSDE', affiliate_number='DEF123456', is_volunteer=False, enabled=False)

    #####################
    # REGISTRO DE PAGOS #
    #####################

    # Creado de tipos de pago
    tipo_pago_honorarios = tipos_pago.create_payment_type("Honorarios")
    tipo_pago_proveedor = tipos_pago.create_payment_type("Proveedor")
    tipo_pago_gastos_varios = tipos_pago.create_payment_type("Gastos Varios")

    # Creado de pagos
    pagos.create_payment(amount=5000, date=datetime(2024, 9, 10), description="Pago realizado", payment_type_id=1, beneficiary_id=1)
    pagos.create_payment(amount=7200, date=datetime.now(), description="El pago fue exitoso", payment_type_id=3, beneficiary_id=1)
    pagos.create_payment(amount=1300, date=datetime(2024, 9, 15), description="Un muy buen pago", payment_type_id=1, beneficiary_id=3)
    pagos.create_payment(amount=10200.50, date=datetime(1999, 2, 20), description="Un pago de un proveedor", payment_type_id=2, beneficiary_id=4)
