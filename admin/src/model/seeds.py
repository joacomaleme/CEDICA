from src.model.auth.operations import permission_operations as permissions
from src.model.auth.operations import role_operations as roles
from src.model.auth.operations import user_operations as users
from src.model.employees.operations import employee_operations as employees
from src.model.employees.operations import job_position_operations as job_positions
from src.model.employees.operations import profession_operations as professions
from src.model.registers.operations import payment_operations as payments
from src.model.registers.operations import payment_type_operations as payment_type
from src.model.generic.operations import address_operations as address
from src.model.generic.operations import locality_operations as locality
from src.model.generic.operations import province_operations as province
from src.model import auth

"""
    IMPORTS DE LAS CLASES PORQUE SI NO EXPLOTA
"""
from src.model.auth.tables.role import Role
from src.model.auth.tables.user import User
from src.model.auth.tables.permission import Permission
from src.model.auth.tables.role_permissions import role_permissions
from src.model.employees.tables.employee import Employee
from src.model.employees.tables.profession import Profession
from src.model.employees.tables.job_position import JobPosition
from src.model.riders.tables.rider import Rider
from src.model.riders.tables.family_allowance_type import FamilyAllowanceType
from src.model.riders.tables.pension_type import PensionType
from src.model.riders.tables.disability_type import DisabilityType
from src.model.riders.tables.horse import Horse
from src.model.riders.tables.school import School
from src.model.riders.tables.guardian import Guardian
from src.model.riders.tables.work_day import WorkDay
from src.model.riders.tables.rider_guardian import RiderGuardian
from src.model.riders.tables.rider_work_day import RiderWorkDay
from src.model.riders.tables.sede import Sede
from src.model.riders.tables.disability_type import DisabilityType
from src.model.riders.tables.disability_diagnosis import DisabilityDiagnosis
from src.model.riders.tables.work_proposal import WorkProposal
from src.model.generic.tables.address import Address
from src.model.generic.tables.document import Document
from src.model.generic.tables.locality import Locality
from src.model.generic.tables.province import Province
from src.model.generic.tables.document_types import DocumentType
from src.model.registers.tables.payment import Payment
from src.model.registers.tables.payment_type import PaymentType




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

    # permisos para riders
    rider_index = permissions.create_permission(name='rider_index')
    rider_show = permissions.create_permission(name='rider_show')
    rider_update = permissions.create_permission(name='rider_update')
    rider_create = permissions.create_permission(name='rider_create')
    rider_destroy = permissions.create_permission(name='rider_destroy')

    # permisos para documentos   ->   Estan hechos pero sin asignar, no se a quienes darlos, si es que siquiera son necesarios.
    document_index = permissions.create_permission(name='document_index')
    document_show = permissions.create_permission(name='document_show')
    document_update = permissions.create_permission(name='document_update')
    document_create = permissions.create_permission(name='document_create')
    document_destroy = permissions.create_permission(name='document_destroy')

    # Asignacion de permisos a roles de usuario
    roles.assign_permission(system_admin, [user_index, user_new, user_update, user_show, user_destroy, employee_index, employee_new, employee_destroy, employee_show, employee_update, payment_index, payment_show, payment_update, payment_create, payment_destroy, rider_index, rider_show, rider_update, rider_create, rider_destroy])
    roles.assign_permission(rol_tecnica, [user_index, user_show, rider_index, rider_show, rider_update, rider_create, rider_destroy])
    roles.assign_permission(rol_ecuestre, [user_index, user_show, rider_index, rider_show])
    roles.assign_permission(rol_voluntariado, user_index)
    roles.assign_permission(rol_administracion, [user_index, user_new, user_update, user_show, employee_index, employee_new, employee_destroy, employee_show, employee_update, payment_index, payment_show, payment_update, payment_create, payment_destroy, rider_index, rider_show, rider_update, rider_create, rider_destroy])

    user1 = users.create_user(alias='Juan', password='123a', email='juan@gmail.com', enabled=True)
    user2 = users.create_user(alias='Martin', password='123a', email='martin@gmail.com', enabled=True, role_id=1)
    user3 = users.create_user(alias='Sofia', password='123a', email='sofia@gmail.com', enabled=True, role_id=2)
    user4 = users.create_user(alias='Pedro', password='123a', email='pedro@gmail.com', enabled=True, role_id=3)

    ############
    # Generics #
    ############
    
    # Crear addresses
    address.create_address("Calle 1", "1433", "1A")
    address.create_address("Calle 7", "2203")
    address.create_address("Calle 13", "473", "4C")
    address.create_address("Calle 5", "1984")
    address.create_address("Calle 44", "3010", "15F")

    # Crear localities
    locality.create_locality("La Plata")
    locality.create_locality("San Carlos")
    locality.create_locality("Villa Adelina")
    locality.create_locality("Boulogne")
    locality.create_locality("Martínez")
    locality.create_locality("Beccar")

    # Crear provinces
    province.create_province("Buenos Aires")
    province.create_province("Córdoba")
    province.create_province("Mendoza")
    province.create_province("Santa Fe")
    province.create_province("Tucumán")

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

    employees.create_employee(name='María', surname='Gómez', dni="45678901", address_id=1, email='maria.gomez@example.com', locality_id=1, phone='1122334455', profession_id=1, job_position_id=2, emergency_contact_name='Juan Gómez', emergency_contact_phone='1198765432', obra_social='OSDE', affiliate_number='ABC123456', is_volunteer=False, enabled=True)
    employees.create_employee(name='Carlos', surname='Pérez', dni="23456789", address_id=2, email='carlos.perez@example.com', locality_id=2, phone='1167891234', profession_id=2, job_position_id=3, emergency_contact_name='Ana Pérez', emergency_contact_phone='1145678901', obra_social='Swiss Medical', affiliate_number='XYZ789012', is_volunteer=False, enabled=True)
    employees.create_employee(name='Lucía', surname='Fernández', dni="34567890", address_id=3, email='lucia.fernandez@example.com', locality_id=3, phone='1156781234', profession_id=3, job_position_id=4, emergency_contact_name='Clara Fernández', emergency_contact_phone='1178901234', obra_social='Galeno', affiliate_number='LMN456789', is_volunteer=True, enabled=True)
    employees.create_employee(name='Javier', surname='López', dni="56789012", address_id=4, email='javier.lopez@example.com', locality_id=4, phone='1123456789', profession_id=4, job_position_id=1, emergency_contact_name='Sofía López', emergency_contact_phone='1124567890', obra_social='OSDE', affiliate_number='DEF123456', is_volunteer=False, enabled=False, user_id=1)

    #####################
    # REGISTRO DE PAGOS #
    #####################

    # Creado de tipos de pago
    tipo_pago_honorarios = payment_type.create_payment_type("Honorarios")
    tipo_pago_proveedor = payment_type.create_payment_type("Proveedor")
    tipo_pago_gastos_varios = payment_type.create_payment_type("Gastos Varios")

    # Creado de pagos
    payments.create_payment(amount=5000, date=datetime(2024, 9, 10), description="Pago realizado", payment_type_id=1, beneficiary_id=1)
    payments.create_payment(amount=7200, date=datetime.now(), description="El pago fue exitoso", payment_type_id=3)
    payments.create_payment(amount=1300, date=datetime(2024, 9, 15), description="Un muy buen pago", payment_type_id=1, beneficiary_id=3)
    payments.create_payment(amount=10200.50, date=datetime(1999, 2, 20), description="Un pago de un proveedor", payment_type_id=2)
