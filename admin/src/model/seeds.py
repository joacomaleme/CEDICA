from src.model.auth.operations import permission_operations as permissions
from src.model.auth.operations import role_operations as roles
from src.model.auth.operations import user_operations as users
from src.model.employees.operations import employee_operations
from src.model.employees.operations import job_position_operations as job_positions
from src.model.employees.operations import profession_operations as professions
from src.model.registers.operations import payment_operations as payments
from src.model.registers.operations import payment_type_operations as payment_type
from src.model.generic.operations import address_operations as address
from src.model.generic.operations import locality_operations as locality
from src.model.generic.operations import province_operations as province
from src.model.riders.operations import rider_operations as riders
from src.model.riders.operations import horse_operations as horses
from src.model.riders.operations import guardian_operations as guardians
from src.model.riders.operations import guardian_rider_operations as guardians_riders
from src.model.riders.operations import work_day_operations as work_days
from src.model.riders.operations import sede_operations as sedes
from src.model.riders.operations import disability_type_operations as disability_types
from src.model.riders.operations import disability_diagnosis_operations as disability_diagnoses
from src.model.riders.operations import work_proposal_operations as work_proposals
from src.model.riders.operations import family_allowance_type_operations as family_allowance_types
from src.model.riders.operations import pension_type_operations as pension_types
from src.model.generic.operations import document_operations as documents
from src.model.generic.operations import document_types_operations as document_types
from src.model.riders.operations import school_operations as schools

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

from datetime import datetime, date



def run():
    ############
    # Usuarios #
    ############

    # Creado de roles
    system_admin = roles.create_role(name='Administrador de Sistema')
    rol_tecnica = roles.create_role(name='Tecnica')
    rol_ecuestre = roles.create_role(name='Ecuestre')
    rol_voluntariado = roles.create_role(name='Voluntariado')
    rol_administracion = roles.create_role(name='Administracion')


    # Creado de permisos para usuarios
    user_permissions = [
        'user_index', 'user_new', 'user_destroy', 'user_update', 'user_show',
        'employee_index', 'employee_new', 'employee_destroy', 'employee_show', 'employee_update',
        'payment_index', 'payment_show', 'payment_update', 'payment_create', 'payment_destroy',
        'rider_index', 'rider_show', 'rider_update', 'rider_create', 'rider_destroy',
        'document_index', 'document_show', 'document_update', 'document_create', 'document_destroy'
    ]

    created_permissions = {}
    for perm in user_permissions:
        created_permissions[perm] = permissions.create_permission(name=perm)



    print("INICIA")

    # Asignacion de permisos a roles de usuario
    roles.assign_permission(system_admin, list(created_permissions.values()))
    roles.assign_permission(rol_tecnica, [created_permissions[p] for p in ['user_index', 'user_show', 'rider_index', 'rider_show', 'rider_update', 'rider_create', 'rider_destroy']])
    roles.assign_permission(rol_ecuestre, [created_permissions[p] for p in ['user_index', 'user_show', 'rider_index', 'rider_show']])
    roles.assign_permission(rol_voluntariado, [created_permissions['user_index']])
    roles.assign_permission(rol_administracion, [created_permissions[p] for p in user_permissions if p not in ['user_destroy']])

    print("INICIA2")


    # Creado de usuarios

    users_data = [
        ('Juan', '123a', 'juan@gmail.com', True, None),
        ('Martin', '123a', 'martin@gmail.com', True, 1),
        ('Sofia', '123a', 'sofia@gmail.com', True, 2),
        ('Pedro', '123a', 'pedro@gmail.com', True, 3),
        ('Ana', '123a', 'ana@gmail.com', True, 4),
        ('Luis', '123a', 'luis@gmail.com', True, 5),
        ('Elena', '123a', 'elena@gmail.com', False, 2),
        ('Carlos', '123a', 'carlos@gmail.com', True, 3),
        ('Maria', '123a', 'maria@gmail.com', True, 1),
        ('Pablo', '123a', 'pablo@gmail.com', True, 5),
        ('Laura', '123a', 'laura@gmail.com', False, 3),
        ('Jorge', '123a', 'jorge@gmail.com', True, 2),
        ('Lucia', '123a', 'lucia@gmail.com', True, 4),
        ('Felipe', '123a', 'felipe@gmail.com', False, 5),
        ('Carolina', '123a', 'carolina@gmail.com', True, 1),
        ('Valentina', '123a', 'valentina@gmail.com', False, 4),
        ('Ricardo', '123a', 'ricardo@gmail.com', True, 2),
        ('Camila', '123a', 'camila@gmail.com', True, 3),
        ('Rodrigo', '123a', 'rodrigo@gmail.com', True, 4),
        ('Andrea', '123a', 'andrea@gmail.com', True, 5),
        ('Sergio', '123a', 'sergio@gmail.com', False, 1),
        ('Claudia', '123a', 'claudia@gmail.com', True, 3),
        ('Fernando', '123a', 'fernando@gmail.com', True, 2),
        ('Patricia', '123a', 'patricia@gmail.com', True, 4),
        ('Oscar', '123a', 'oscar@gmail.com', False, 5),
        ('Daniel', '123a', 'daniel@gmail.com', True, 1),
        ('Paula', '123a', 'paula@gmail.com', True, 2),
        ('Emilio', '123a', 'emilio@gmail.com', True, 3),
        ('Gabriela', '123a', 'gabriela@gmail.com', True, 4),
        ('Esteban', '123a', 'esteban@gmail.com', False, 5),
        ('Santiago', '123a', 'santiago@gmail.com', True, None),
        ('Graciela', '123a', 'graciela@gmail.com', False, 3),
        ('Javier', '123a', 'javier@gmail.com', True, 2),
        ('Marta', '123a', 'marta@gmail.com', True, 1),
        ('Miguel', '123a', 'miguel@gmail.com', True, 4),
        ('Florencia', '123a', 'florencia@gmail.com', True, 5),
        ('Hugo', '123a', 'hugo@gmail.com', False, 3),
        ('Alberto', '123a', 'alberto@gmail.com', True, 2),
        ('Natalia', '123a', 'natalia@gmail.com', True, 5),
        ('Francisco', '123a', 'francisco@gmail.com', True, 4),
        ('Victoria', '123a', 'victoria@gmail.com', False, 1),
        ('Ramiro', '123a', 'ramiro@gmail.com', True, 3),
        ('Silvia', '123a', 'silvia@gmail.com', True, 2),
        ('Nicolas', '123a', 'nicolas@gmail.com', True, 1),
        ('Alicia', '123a', 'alicia@gmail.com', True, 5),
        ('Julian', '123a', 'julian@gmail.com', False, 4),
        ('Monica', '123a', 'monica@gmail.com', True, 3),
        ('Sebastian', '123a', 'sebastian@gmail.com', True, 2),
        ('Cecilia', '123a', 'cecilia@gmail.com', True, 1),
        ('Roberto', '123a', 'roberto@gmail.com', False, 4),
        ('Isabel', '123a', 'isabel@gmail.com', True, 3),
        ('Guillermo', '123a', 'guillermo@gmail.com', True, 5),
        ('Pamela', '123a', 'pamela@gmail.com', True, None),
        ('Leandro', '123a', 'leandro@gmail.com', True, 1),
        ('Viviana', '123a', 'viviana@gmail.com', True, 4),
        ('Cristina', '123a', 'cristina@gmail.com', True, 3),
        ('Hernan', '123a', 'hernan@gmail.com', False, 2),
        ('Federico', '123a', 'federico@gmail.com', True, 5),
        ('Belen', '123a', 'belen@gmail.com', True, 1),
        ('Ignacio', '123a', 'ignacio@gmail.com', True, 4),
        ('Daniela', '123a', 'daniela@gmail.com', False, 3),
        ('Mariano', '123a', 'mariano@gmail.com', True, 2),
        ('Nora', '123a', 'nora@gmail.com', True, 5),
        ('Maximiliano', '123a', 'maximiliano@gmail.com', True, None),
        ('Damian', '123a', 'damian@gmail.com', True, 3),
        ('Antonella', '123a', 'antonella@gmail.com', False, 2),
        ('Ramona', '123a', 'ramona@gmail.com', True, 5),
        ('Lucas', '123a', 'lucas@gmail.com', True, 4),
        ('Julia', '123a', 'julia@gmail.com', True, 3),
        ('Franco', '123a', 'franco@gmail.com', False, 2),
        ('Micaela', '123a', 'micaela@gmail.com', True, 1),
        ('Bruno', '123a', 'bruno@gmail.com', True, 5),
        ('Agustina', '123a', 'agustina@gmail.com', True, 4),
        ('Kevin', '123a', 'kevin@gmail.com', True, None),
        ('Tamara', '123a', 'tamara@gmail.com', True, 2),
        ('Ezequiel', '123a', 'ezequiel@gmail.com', False, 1),
        ('Mauro', '123a', 'mauro@gmail.com', True, 3),
        ('Vanesa', '123a', 'vanesa@gmail.com', True, 4),
        ('Brenda', '123a', 'brenda@gmail.com', True, 5),
        ('Adriana', '123a', 'adriana@gmail.com', True, 1),
        ('Leonardo', '123a', 'leonardo@gmail.com', False, 2),
        ('Milagros', '123a', 'milagros@gmail.com', True, 3),
        ('Sabrina', '123a', 'sabrina@gmail.com', True, 5),
        ('Lautaro', '123a', 'lautaro@gmail.com', True, 1),
        ('Evelyn', '123a', 'evelyn@gmail.com', False, 4),
        ('Diego', '123a', 'diego@gmail.com', True, 2),
        ('Antonieta', '123a', 'antonieta@gmail.com', True, 3),
        ('Gonzalo', '123a', 'gonzalo@gmail.com', True, 5),
        ('Sonia', '123a', 'sonia@gmail.com', True, None),
        ('Facundo', '123a', 'facundo@gmail.com', True, 1),
        ('Melina', '123a', 'melina@gmail.com', True, 2),
        ('Emmanuel', '123a', 'emmanuel@gmail.com', True, 4),
    ]
    print("INICIA4")

    for user_data in users_data:
        users.create_user(alias=user_data[0], password=user_data[1], email=user_data[2], enabled=user_data[3], role_id=user_data[4])

    print("INICIA3")

    ############
    # Generics #
    ############
    
    # Crear addresses
    addresses = [
        ("Calle 1", "1433", "1A"),
        ("Calle 7", "2203", None),
        ("Calle 13", "473", "4C"),
        ("Calle 5", "1984", None),
        ("Calle 44", "3010", "15F"),
        ("Avenida Libertador", "5678", "8B"),
        ("Pasaje del Sol", "123", None),
        ("Ruta 2", "Km 65", None),
        ("Calle San Martín", "789", "3D"),
        ("Avenida Mayo", "1122", "12A"),
    ]
    for addr in addresses:
        address.create_address(*addr)

    # Crear localities
    localities = [
        "La Plata", "San Carlos", "Villa Adelina", "Boulogne", "Martínez", "Beccar",
        "Quilmes", "Avellaneda", "Lanús", "Banfield", "Lomas de Zamora", "Adrogué"
    ]
    for loc in localities:
        locality.create_locality(loc)

    # Crear provinces
    provinces = [
        "Buenos Aires", "Córdoba", "Mendoza", "Santa Fe", "Tucumán",
        "Entre Ríos", "Salta", "Chaco", "Misiones", "San Juan"
    ]
    for prov in provinces:
        province.create_province(prov)




    #############
    # Empleados #
    #############

    # Creado de profesiones
    professions_list = [
        "Médico/a", "Docente", "Psicólogo/a", "Otro", "Fisioterapeuta",
        "Terapeuta Ocupacional", "Trabajador/a Social", "Enfermero/a", "Nutricionista"
    ]
    for prof in professions_list:
        professions.create_profession(prof)

    # Creado de posiciones
    job_positions_list = [
        "Terapeuta", "Domador", "Profesor de Equitación", "Otro",
        "Coordinador de Programas", "Asistente Administrativo", "Cuidador de Caballos",
        "Voluntario", "Recepcionista", "Mantenimiento"
    ]
    for job in job_positions_list:
        job_positions.create_job_position(job)

    # Creado de empleados
    employees = [
        {
            "name": "Juan",
            "surname": "Pérez",
            "dni": "12345678",
            "address_id": 1,
            "email": "juan.perez@example.com",
            "locality_id": 1,
            "phone": "555-0123",
            "profession_id": 1,
            "job_position_id": 1,
            "emergency_contact_name": "María Pérez",
            "emergency_contact_phone": "555-9876",
            "obra_social": "Obra Social A",
            "affiliate_number": "A123456",
            "is_volunteer": False,
            "user_id": 1,
            "enabled": True,
            "start_date": datetime(2023, 1, 15),
            "end_date": None
        },
        {
            "name": "Lucía",
            "surname": "González",
            "dni": "23456789",
            "address_id": 2,
            "email": "lucia.gonzalez@example.com",
            "locality_id": 2,
            "phone": "555-0234",
            "profession_id": 2,
            "job_position_id": 2,
            "emergency_contact_name": "Pedro González",
            "emergency_contact_phone": "555-8765",
            "obra_social": "Obra Social B",
            "affiliate_number": "B234567",
            "is_volunteer": True,
            "user_id": 2,
            "enabled": True,
            "start_date": datetime(2023, 2, 1),
            "end_date": None
        },
        {
            "name": "Carlos",
            "surname": "Martínez",
            "dni": "34567890",
            "address_id": 3,
            "email": "carlos.martinez@example.com",
            "locality_id": 3,
            "phone": "555-0345",
            "profession_id": 3,
            "job_position_id": 3,
            "emergency_contact_name": "Ana Martínez",
            "emergency_contact_phone": "555-7654",
            "obra_social": "Obra Social C",
            "affiliate_number": "C345678",
            "is_volunteer": False,
            "user_id": 3,
            "enabled": True,
            "start_date": datetime(2023, 3, 10),
            "end_date": None
        },
        {
            "name": "Sofía",
            "surname": "López",
            "dni": "45678901",
            "address_id": 4,
            "email": "sofia.lopez@example.com",
            "locality_id": 4,
            "phone": "555-0456",
            "profession_id": 1,
            "job_position_id": 4,
            "emergency_contact_name": "Luis López",
            "emergency_contact_phone": "555-6543",
            "obra_social": "Obra Social D",
            "affiliate_number": "D456789",
            "is_volunteer": True,
            "user_id": 4,
            "enabled": True,
            "start_date": datetime(2023, 4, 20),
            "end_date": None
        },
        {
            "name": "Andrés",
            "surname": "Hernández",
            "dni": "56789012",
            "address_id": 5,
            "email": "andres.hernandez@example.com",
            "locality_id": 5,
            "phone": "555-0567",
            "profession_id": 2,
            "job_position_id": 5,
            "emergency_contact_name": "Clara Hernández",
            "emergency_contact_phone": "555-5432",
            "obra_social": "Obra Social E",
            "affiliate_number": "E567890",
            "is_volunteer": False,
            "user_id": 5,
            "enabled": True,
            "start_date": datetime(2023, 5, 15),
            "end_date": None
        },
        {
            "name": "María",
            "surname": "Díaz",
            "dni": "67890123",
            "address_id": 6,
            "email": "maria.diaz@example.com",
            "locality_id": 6,
            "phone": "555-0678",
            "profession_id": 3,
            "job_position_id": 1,
            "emergency_contact_name": "Jorge Díaz",
            "emergency_contact_phone": "555-4321",
            "obra_social": "Obra Social F",
            "affiliate_number": "F678901",
            "is_volunteer": True,
            "user_id": 6,
            "enabled": True,
            "start_date": datetime(2023, 6, 10),
            "end_date": None
        },
        {
            "name": "Fernando",
            "surname": "Gutiérrez",
            "dni": "78901234",
            "address_id": 7,
            "email": "fernando.gutierrez@example.com",
            "locality_id": 7,
            "phone": "555-0789",
            "profession_id": 1,
            "job_position_id": 2,
            "emergency_contact_name": "Patricia Gutiérrez",
            "emergency_contact_phone": "555-3210",
            "obra_social": "Obra Social G",
            "affiliate_number": "G789012",
            "is_volunteer": False,
            "user_id": 7,
            "enabled": True,
            "start_date": datetime(2023, 7, 5),
            "end_date": None
        },
        {
            "name": "Valentina",
            "surname": "Morales",
            "dni": "89012345",
            "address_id": 8,
            "email": "valentina.morales@example.com",
            "locality_id": 8,
            "phone": "555-0890",
            "profession_id": 2,
            "job_position_id": 3,
            "emergency_contact_name": "Marco Morales",
            "emergency_contact_phone": "555-2109",
            "obra_social": "Obra Social H",
            "affiliate_number": "H890123",
            "is_volunteer": True,
            "user_id": 8,
            "enabled": True,
            "start_date": datetime(2023, 8, 15),
            "end_date": None
        },
        {
            "name": "Diego",
            "surname": "Castro",
            "dni": "90123456",
            "address_id": 9,
            "email": "diego.castro@example.com",
            "locality_id": 9,
            "phone": "555-0901",
            "profession_id": 3,
            "job_position_id": 4,
            "emergency_contact_name": "Gloria Castro",
            "emergency_contact_phone": "555-1098",
            "obra_social": "Obra Social I",
            "affiliate_number": "I901234",
            "is_volunteer": False,
            "user_id": 9,
            "enabled": True,
            "start_date": datetime(2023, 9, 10),
            "end_date": None
        },
        {
            "name": "Cecilia",
            "surname": "Paredes",
            "dni": "01234567",
            "address_id": 10,
            "email": "cecilia.paredes@example.com",
            "locality_id": 10,
            "phone": "555-1010",
            "profession_id": 1,
            "job_position_id": 1,
            "emergency_contact_name": "Ricardo Paredes",
            "emergency_contact_phone": "555-8765",
            "obra_social": "Obra Social J",
            "affiliate_number": "J012345",
            "is_volunteer": True,
            "user_id": 10,
            "enabled": True,
            "start_date": datetime(2023, 10, 1),
            "end_date": None
        },
    ]

    print("MITAD")

    for emp in employees:
        employee_operations.create_employee(
            name=emp["name"],
            surname=emp["surname"],
            dni=emp["dni"],
            address_id=emp["address_id"],
            email=emp["email"],
            locality_id=emp["locality_id"],
            phone=emp["phone"],
            profession_id=emp["profession_id"],
            job_position_id=emp["job_position_id"],
            emergency_contact_name=emp["emergency_contact_name"],
            emergency_contact_phone=emp["emergency_contact_phone"],
            obra_social=emp["obra_social"],
            affiliate_number=emp["affiliate_number"],
            is_volunteer=emp["is_volunteer"],
            user_id=emp["user_id"],
            enabled=emp["enabled"],
            start_date=emp["start_date"],
            end_date=emp["end_date"],
        )

    #####################
    # REGISTRO DE PAGOS #
    #####################

    # Creado de tipos de pago
    payment_types = ["Honorarios", "Proveedor", "Gastos Varios", "Donación", "Materiales", "Alquiler"]
    for pt in payment_types:
        payment_type.create_payment_type(pt)

    # Creado de pagos
    payments_data = [
        (5000, datetime(2024, 9, 10), "Pago realizado", 1, 1),
        (7200, datetime.now(), "El pago fue exitoso", 3, None),
        (1300, datetime(2024, 9, 15), "Un muy buen pago", 1, 3),
        (10200.50, datetime(1999, 2, 20), "Un pago de un proveedor", 2, None),
        (3500, datetime(2024, 10, 1), "Donación mensual", 4, None),
        (2800, datetime(2024, 10, 5), "Compra de materiales", 5, 2),
        (15000, datetime(2024, 10, 12), "Alquiler de instalaciones", 6, None),
        (4200, datetime(2024, 10, 18), "Honorarios profesionales", 1, 4),
    ]
    for payment in payments_data:
        payments.create_payment(*payment)


    ##################
    # Riders Section #
    ##################

    # Create disability types
    disability_types_list = ["Física", "Intelectual", "Sensorial", "Psíquica", "Visceral", "Múltiple"]
    for dt in disability_types_list:
        disability_types.create_disability_type(dt)

    # Create disability diagnoses
    diagnoses_list = ["Parálisis Cerebral", "Síndrome de Down", "Autismo", "Lesión Medular", "Esclerosis Múltiple", "Distrofia Muscular"]
    for diag in diagnoses_list:
        disability_diagnoses.create_disability_diagnosis(diag)

    # Create horses
    horses_data = [
        ("Luna", "Yegua", "Criolla", 12, True),
        ("Trueno", "Caballo", "Cuarto de Milla", 8, True),
        ("Estrella", "Yegua", "Appaloosa", 10, False),
        ("Relámpago", "Caballo", "Árabe", 6, True),
        ("Tormenta", "Yegua", "Cuarto de Milla", 6, True),
        ("Locura", "Yegua", "Pinto", 9, True),
        ("Rayo", "Caballo", "Appaloosa", 10, True),
        ("Fuego", "Caballo", "Pinto", 7, False)
    ]
    for horse in horses_data:
        horses.create_horse(*horse)

    # Create sedes
    sedes_list = ["Sede Central", "Sede Norte", "Sede Sur", "Sede Este", "Sede Oeste"]
    for sede in sedes_list:
        sedes.create_sede(sede)

    # Create work days
    days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
    for day in days:
        work_days.create_work_day(day)

    # Create work proposals
    proposals = ["Hipoterapia", "Monta Terapéutica", "Equitación Adaptada", "Volteo Adaptado", "Carruaje Adaptado"]
    for prop in proposals:
        work_proposals.create_work_proposal(prop)

    # Create family allowance types
    allowance_types = ["Universal", "Discapacidad", "Escolar"]
    for at in allowance_types:
        family_allowance_types.create_family_allowance_type(at)

    # Create pension types
    pension_types_list = ["Nacional", "Provincial"]
    for pt in pension_types_list:
        pension_types.create_pension_type(pt)

    # Create schools

    schools.create_school(name="Greenwood High School", address="123 Oak Street, Springfield", phone="123-456-7890", observations="Focus on STEM programs.")
    schools.create_school(name="Sunnydale Elementary", address="456 Maple Avenue, Rivertown", phone="987-654-3210", observations="Strong emphasis on arts and music.")
    schools.create_school(name="Lakeside Academy", address="789 Pine Road, Lakeview", phone="555-123-4567", observations="Offers international exchange programs.")
    schools.create_school(name="Hillcrest Secondary School", address="321 Cedar Drive, Mountain City", phone="444-987-6543", observations="Known for sports excellence.")
    schools.create_school(name="Riverbank Primary School", address="654 Elm Street, Rivertown", phone="333-555-7777", observations="Bilingual education offered.")
    schools.create_school(name="Maplewood High School", address="987 Birch Lane, Greenwood", phone="222-666-8888", observations="Top ranking in local exams.")
    schools.create_school(name="Crestview College", address="432 Spruce Avenue, Crestview", phone="777-888-9999", observations="Advanced vocational training programs.")
    schools.create_school(name="Westfield Technical School", address="876 Willow Road, Westfield", phone="111-333-5555", observations="Focus on technology and trades.")
    schools.create_school(name="Eastfield Technical School", address="679 Road Willow, Eastfield", phone="555-533-3111", observations=".sedart dna yholonhcet no sucoF")
    schools.create_school(name="Blue Ridge Middle School", address="101 Mountain View Drive, Blue Ridge", phone="123-789-4560", observations="Focus on outdoor education and environmental awareness.")
    schools.create_school(name="Willowbrook Primary School", address="567 Oak Lane, Willowbrook", phone="234-567-8901", observations="Renowned for inclusive education and community involvement.")
    schools.create_school(name="Evergreen High School", address="890 Forest Road, Pinehill", phone="345-678-9012", observations="Known for their excellence in science and math competitions.")
    schools.create_school(name="Meadowview College", address="234 Sunrise Avenue, Meadowview", phone="456-789-0123", observations="Highly regarded for their business and entrepreneurship programs.")
    schools.create_school(name="Brookstone Elementary", address="456 Riverbend Road, Brookstone", phone="567-890-1234", observations="Arts-focused school with regular community theater performances.")
    schools.create_school(name="Pinecrest Secondary School", address="789 Summit Way, Pinecrest", phone="678-901-2345", observations="Emphasis on leadership programs and student government.")
    schools.create_school(name="Clearwater Technical Institute", address="101 Marina Drive, Clearwater", phone="789-012-3456", observations="Specializes in IT and software development courses.")
    schools.create_school(name="Sunrise High School", address="202 Hilltop Road, Sunrise City", phone="890-123-4567", observations="Focus on academic excellence with extensive AP courses.")
    schools.create_school(name="Shady Grove Academy", address="345 Grove Lane, Shady Grove", phone="901-234-5678", observations="Known for innovative STEM curriculum and modern labs.")
    schools.create_school(name="Silver Lake Prep", address="567 Silver Lake Boulevard, Silver City", phone="012-345-6789", observations="Offers a preparatory curriculum with a focus on college readiness.")
    schools.create_school(name="Oakwood High School", address="890 Woodland Drive, Oakwood", phone="234-456-7890", observations="Strong athletic programs with state championship teams.")
    schools.create_school(name="Harborview Academy", address="123 Harborview Road, Seaview", phone="345-567-8901", observations="Focus on marine biology and oceanography studies.")
    schools.create_school(name="Riverside High School", address="567 Riverside Drive, Riverside", phone="456-678-9012", observations="Offers a comprehensive arts program including music and visual arts.")
    schools.create_school(name="Bayside Elementary", address="789 Seaside Boulevard, Bayside", phone="567-789-0123", observations="Known for their early childhood education excellence.")
    schools.create_school(name="Mountainview Secondary School", address="101 Peak Road, Mountainview", phone="678-890-1234", observations="Highly regarded for its rigorous academic and extracurricular programs.")
    schools.create_school(name="Woodland Park Academy", address="345 Woodland Avenue, Woodside", phone="789-901-2345", observations="Focus on sustainability and environmental science.")
    schools.create_school(name="Bridgewater High School", address="678 Bridgewater Lane, Bridgewater", phone="890-012-3456", observations="Offers advanced courses in technology and engineering.")
    schools.create_school(name="Elmwood Technical School", address="123 Elmwood Street, Green Valley", phone="012-345-6789", observations="Known for trade programs in automotive and construction fields.")
    schools.create_school(name="Cedar Grove College", address="456 Cedar Grove Road, Cedarville", phone="234-567-8901", observations="Specializes in liberal arts and humanities.")
    schools.create_school(name="Hillside Prep", address="789 Hillside Boulevard, Hilltown", phone="345-678-9012", observations="Prep school with an emphasis on college preparatory and advanced placement courses.")




    # Create riders
    # Example 1
    riders.create_rider(
        name="John", last_name="Doe", dni="12345678", age=25, birth_date=date(1999, 5, 14),
        birth_locality_id=1, birth_province_id=1, address_id=1, current_locality_id=2,
        current_province_id=2, phone="555-1234", emergency_contact_name="Jane Doe",
        emergency_contact_phone="555-5678", active=True, sede="North", has_scholarship=True,
        scholarship_percentage=50.0, has_disability_certificate=False, disability_diagnosis_id=None,
        disability_type_id=None, receives_family_allowance=False, family_allowance_type_id=None,
        receives_pension=False, pension_type_id=None, health_insurance="HealthPlus",
        affiliate_number="H123456", has_guardianship=True, school_id=3, current_grade="Grade 10",
        attending_professionals="Dr. Smith", work_proposal="Therapeutic riding", teacher_id=1,
        horse_conductor_id=2, horse_id=1, track_assistant_id=3
    )

    # Example 2
    riders.create_rider(
        name="Emily", last_name="Smith", dni="87654321", age=30, birth_date=date(1994, 8, 10),
        birth_locality_id=2, birth_province_id=3, address_id=2, current_locality_id=4,
        current_province_id=3, phone="555-7890", emergency_contact_name="Peter Smith",
        emergency_contact_phone="555-8765", active=True, sede="East", has_scholarship=False,
        scholarship_percentage=None, has_disability_certificate=True, disability_diagnosis_id=1,
        disability_type_id=2, receives_family_allowance=True, family_allowance_type_id=1,
        receives_pension=False, pension_type_id=None, health_insurance="MediCare",
        affiliate_number="MC56789", has_guardianship=True, school_id=5, current_grade="Grade 8",
        attending_professionals="Dr. Brown", work_proposal="Social interaction", teacher_id=2,
        horse_conductor_id=3, horse_id=2, track_assistant_id=4
    )

    # Example 3
    riders.create_rider(
        name="Lucas", last_name="Johnson", dni="65432198", age=20, birth_date=date(2004, 1, 21),
        birth_locality_id=3, birth_province_id=2, address_id=3, current_locality_id=5,
        current_province_id=4, phone="555-4321", emergency_contact_name="Sarah Johnson",
        emergency_contact_phone="555-3210", active=False, sede="South", has_scholarship=False,
        scholarship_percentage=None, has_disability_certificate=False, disability_diagnosis_id=None,
        disability_type_id=None, receives_family_allowance=True, family_allowance_type_id=2,
        receives_pension=True, pension_type_id=1, health_insurance="HealthCare",
        affiliate_number="HC12345", has_guardianship=True, school_id=6, current_grade="Grade 12",
        attending_professionals="Dr. White", work_proposal="Cognitive development", teacher_id=3,
        horse_conductor_id=1, horse_id=3, track_assistant_id=5
    )

    # Example 4
    riders.create_rider(
        name="Sophia", last_name="Brown", dni="87651234", age=28, birth_date=date(1996, 11, 15),
        birth_locality_id=4, birth_province_id=1, address_id=4, current_locality_id=1,
        current_province_id=5, phone="555-6543", emergency_contact_name="James Brown",
        emergency_contact_phone="555-9876", active=True, sede="Central", has_scholarship=True,
        scholarship_percentage=75.0, has_disability_certificate=True, disability_diagnosis_id=2,
        disability_type_id=1, receives_family_allowance=False, family_allowance_type_id=None,
        receives_pension=True, pension_type_id=2, health_insurance="PrimeHealth",
        affiliate_number="PH87654", has_guardianship=True, school_id=7, current_grade="Grade 11",
        attending_professionals="Dr. Green", work_proposal="Motor skills", teacher_id=4,
        horse_conductor_id=5, horse_id=4, track_assistant_id=6
    )

    # Example 5
    riders.create_rider(
        name="James", last_name="Wilson", dni="99887766", age=22, birth_date=date(2002, 3, 5),
        birth_locality_id=5, birth_province_id=4, address_id=5, current_locality_id=6,
        current_province_id=6, phone="555-1111", emergency_contact_name="Anna Wilson",
        emergency_contact_phone="555-2222", active=False, sede="West", has_scholarship=False,
        scholarship_percentage=None, has_disability_certificate=False, disability_diagnosis_id=None,
        disability_type_id=None, receives_family_allowance=True, family_allowance_type_id=3,
        receives_pension=False, pension_type_id=None, health_insurance="OptiCare",
        affiliate_number="OC54321", has_guardianship=True, school_id=8, current_grade="Grade 9",
        attending_professionals="Dr. Blue", work_proposal="Communication skills", teacher_id=5,
        horse_conductor_id=6, horse_id=5, track_assistant_id=7
    )

    # Example 6
    riders.create_rider(
        name="Olivia", last_name="Garcia", dni="44556677", age=19, birth_date=date(2005, 7, 19),
        birth_locality_id=6, birth_province_id=7, address_id=6, current_locality_id=7,
        current_province_id=3, phone="555-3333", emergency_contact_name="Carlos Garcia",
        emergency_contact_phone="555-4444", active=True, sede="North", has_scholarship=True,
        scholarship_percentage=100.0, has_disability_certificate=True, disability_diagnosis_id=3,
        disability_type_id=3, receives_family_allowance=False, family_allowance_type_id=None,
        receives_pension=True, pension_type_id=1, health_insurance="GlobalCare",
        affiliate_number="GC12321", has_guardianship=True, school_id=9, current_grade="Grade 7",
        attending_professionals="Dr. Red", work_proposal="Behavioral therapy", teacher_id=6,
        horse_conductor_id=7, horse_id=6, track_assistant_id=8
    )

    # Example 7
    riders.create_rider(
        name="Michael", last_name="Martinez", dni="11223344", age=24, birth_date=date(2000, 12, 10),
        birth_locality_id=7, birth_province_id=8, address_id=7, current_locality_id=8,
        current_province_id=9, phone="555-5555", emergency_contact_name="Laura Martinez",
        emergency_contact_phone="555-6666", active=False, sede="South", has_scholarship=False,
        scholarship_percentage=None, has_disability_certificate=False, disability_diagnosis_id=None,
        disability_type_id=None, receives_family_allowance=True, family_allowance_type_id=2,
        receives_pension=False, pension_type_id=None, health_insurance="SecureHealth",
        affiliate_number="SH23456", has_guardianship=True, school_id=10, current_grade="Grade 6",
        attending_professionals="Dr. Yellow", work_proposal="Physical therapy", teacher_id=7,
        horse_conductor_id=8, horse_id=7, track_assistant_id=9
    )

    # Example 8
    riders.create_rider(
        name="Emma", last_name="Lopez", dni="22334455", age=26, birth_date=date(1998, 4, 18),
        birth_locality_id=8, birth_province_id=9, address_id=8, current_locality_id=9,
        current_province_id=10, phone="555-7777", emergency_contact_name="David Lopez",
        emergency_contact_phone="555-8888", active=True, sede="Central", has_scholarship=False,
        scholarship_percentage=None, has_disability_certificate=True, disability_diagnosis_id=4,
        disability_type_id=2, receives_family_allowance=True, family_allowance_type_id=3,
        receives_pension=True, pension_type_id=2, health_insurance="BlueCare",
        affiliate_number="BC98765", has_guardianship=True, school_id=11, current_grade="Grade 5",
        attending_professionals="Dr. Purple", work_proposal="Language development", teacher_id=8,
        horse_conductor_id=9, horse_id=8, track_assistant_id=10
    )


    # Create 16 guardians
    guardian_data = [
        # Guardians for Rider 1
        ("Juan", "Gomez", 12345678, 1, 1, 1, "cel1", "juan.gomez@mail.com", "Primario", "Carpenter"),
        ("Maria", "Perez", 23456789, 1, 1, 1, "cel12", "maria.perez@mail.com", "Secundario", "Teacher"),
    
        # Guardians for Rider 2
        ("Carlos", "Lopez", 34567890, 2, 2, 2, "cel3", "carlos.lopez@mail.com", "Universitario", "Engineer"),
        ("Ana", "Martinez", 45678901, 2, 2, 2, "cel4", "ana.martinez@mail.com", "Primario", "Nurse"),
    
        # Guardians for Rider 3
        ("Roberto", "Fernandez", 56789012, 3, 3, 3, "cel5", "roberto.fernandez@mail.com", "Terciario", "Plumber"),
        ("Lucia", "Gonzalez", 67890123, 3, 3, 3, "cel6", "lucia.gonzalez@mail.com", "Secundario", "Accountant"),
    
        # Guardians for Rider 4
        ("Jose", "Rodriguez", 78901234, 4, 4, 4, "cel7", "jose.rodriguez@mail.com", "Universitario", "Architect"),
        ("Laura", "Torres", 89012345, 4, 4, 4, "cel8", "laura.torres@mail.com", "Primario", "Baker"),
    
        # Guardians for Rider 5
        ("Luis", "Castro", 90123456, 5, 5, 5, "cel9", "luis.castro@mail.com", "Secundario", "Mechanic"),
        ("Elena", "Diaz", 11234567, 5, 5, 5, "cel10", "elena.diaz@mail.com", "Terciario", "Doctor"),
    
        # Guardians for Rider 6
        ("Mario", "Sanchez", 22345678, 6, 6, 6, "cel11", "mario.sanchez@mail.com", "Universitario", "Lawyer"),
        ("Patricia", "Vega", 33456789, 6, 6, 6, "cel12", "patricia.vega@mail.com", "Primario", "Secretary"),
    
        # Guardians for Rider 7
        ("Pedro", "Molina", 44567890, 7, 7, 7, "cel13", "pedro.molina@mail.com", "Secundario", "Driver"),
        ("Sofia", "Ramos", 55678901, 7, 7, 7, "cel14", "sofia.ramos@mail.com", "Universitario", "Teacher"),
    
        # Guardians for Rider 8
        ("Ricardo", "Ruiz", 66789012, 8, 8, 8, "cel15", "ricardo.ruiz@mail.com", "Terciario", "Electrician"),
        ("Angela", "Morales", 77890123, 8, 8, 8, "cel16", "angela.morales@mail.com", "Secundario", "Psychologist")
    ]
    # Create guardians and assign them to riders
    for i, data in enumerate(guardian_data):
        name, last_name, dni, address_id, locality_id, province_id, phone, email, education_level, occupation = data
        guardian = guardians.create_guardian(name, last_name, dni, address_id, locality_id, province_id, phone, email, education_level, occupation)
    
        # Assign guardians to riders (each rider gets 2 guardians)
        rider_id = (i // 2) + 1  # Riders 1..8
        relationship = "Father" if i % 2 == 0 else "Mother"
        guardians_riders.assign_guardian_to_rider(rider_id=rider_id, guardian_id=guardian.id, relationship=relationship)
    
    print("FINAL")