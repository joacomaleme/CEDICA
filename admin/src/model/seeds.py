from src.model.auth.operations import permission_operations as permissions
from src.model.auth.operations import role_operations as roles
from src.model.auth.operations import user_operations as users
from src.model.employees.operations import employee_operations
from src.model.employees.operations import job_position_operations as job_positions
from src.model.employees.operations import profession_operations as professions
from src.model.registers.operations import payment_operations as payments
from src.model.registers.operations import payment_type_operations as payment_type
from src.model.registers.operations import collection_operations as collections
from src.model.registers.operations import collection_medium_operations as collection_medium
from src.model.generic.operations import address_operations as address
from src.model.generic.operations import locality_operations as locality
from src.model.generic.operations import province_operations as province
from src.model.generic.operations import document_operations as documents
from src.model.generic.operations import document_types_operations as document_types
from src.model.generic.operations import sede_operations as sedes
from src.model.generic.operations import work_proposal_operations as work_proposals
from src.model.riders.operations import rider_operations as riders
from src.model.riders.operations import work_day_operations as work_days
from src.model.riders.operations import disability_type_operations as disability_types
from src.model.riders.operations import disability_diagnosis_operations as disability_diagnoses
from src.model.riders.operations import family_allowance_type_operations as family_allowance_types
from src.model.riders.operations import pension_type_operations as pension_types
from src.model.riders.operations import school_operations as schools
from src.model.horses.operations import horse_operations as horses

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
from src.model.horses.tables.horse import Horse
from src.model.riders.tables.school import School
from src.model.riders.tables.work_day import WorkDay
from src.model.riders.tables.rider_work_day import RiderWorkDay
from src.model.generic.tables.sede import Sede
from src.model.riders.tables.disability_type import DisabilityType
from src.model.riders.tables.disability_diagnosis import DisabilityDiagnosis
from src.model.generic.tables.work_proposal import WorkProposal
from src.model.generic.tables.address import Address
from src.model.generic.tables.document import Document
from src.model.generic.tables.locality import Locality
from src.model.generic.tables.province import Province
from src.model.generic.tables.document_types import DocumentType
from src.model.registers.tables.payment import Payment
from src.model.registers.tables.payment_type import PaymentType

from datetime import datetime, date, timedelta

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
        'employee_index', 'employee_destroy', 'employee_create', 'employee_show', 'employee_update',
        'payment_index', 'payment_show', 'payment_update', 'payment_create', 'payment_destroy',
        'rider_index', 'rider_show', 'rider_update', 'rider_create', 'rider_destroy',
        'employee_document', 'horse_document', 'rider_document',
        'collection_index', 'collection_show', 'collection_update', 'collection_create', 'collection_destroy',
        'horse_index', 'horse_show', 'horse_update', 'horse_create', 'horse_destroy'
    ]

    created_permissions = {}
    for perm in user_permissions:
        created_permissions[perm] = permissions.create_permission(name=perm)

    # Asignacion de permisos a roles de usuario
    roles.assign_permission(system_admin, list(created_permissions.values()))
    roles.assign_permission(rol_tecnica, [created_permissions[p] for p in ['user_index', 'user_show', 'rider_index', 'rider_show', 'rider_update', 'rider_create', 'rider_destroy', 'collection_index', 'collection_show', 'horse_index', 'horse_show']])
    roles.assign_permission(rol_ecuestre, [created_permissions[p] for p in ['user_index', 'user_show', 'rider_index', 'rider_show', 'horse_index', 'horse_show', 'horse_update', 'horse_create', 'horse_destroy']])
    roles.assign_permission(rol_voluntariado, [created_permissions['user_index']])
    roles.assign_permission(rol_administracion, [created_permissions[p] for p in user_permissions if p not in ['user_destroy', 'horse_update', 'horse_create', 'horse_destroy']])

    # Creado de usuarios
    users_data = [
        ('Juan', '123a', 'juan@gmail.com', True, 1),
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
        ('Santiago', '123a', 'santiago@gmail.com', True, 2),
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
        ('Pamela', '123a', 'pamela@gmail.com', True, 3),
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
        ('Maximiliano', '123a', 'maximiliano@gmail.com', True, 1),
        ('Damian', '123a', 'damian@gmail.com', True, 3),
        ('Antonella', '123a', 'antonella@gmail.com', False, 2),
        ('Ramona', '123a', 'ramona@gmail.com', True, 5),
        ('Lucas', '123a', 'lucas@gmail.com', True, 4),
        ('Julia', '123a', 'julia@gmail.com', True, 3),
        ('Franco', '123a', 'franco@gmail.com', False, 2),
        ('Micaela', '123a', 'micaela@gmail.com', True, 1),
        ('Bruno', '123a', 'bruno@gmail.com', True, 5),
        ('Agustina', '123a', 'agustina@gmail.com', True, 4),
        ('Kevin', '123a', 'kevin@gmail.com', True, 3),
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
        ('Sonia', '123a', 'sonia@gmail.com', True, 4),
        ('Facundo', '123a', 'facundo@gmail.com', True, 1),
        ('Melina', '123a', 'melina@gmail.com', True, 2),
        ('Emmanuel', '123a', 'emmanuel@gmail.com', True, 4),
    ]
    for user_data in users_data:
        users.create_user(alias=user_data[0], password=user_data[1], email=user_data[2], enabled=user_data[3], role_id=user_data[4])

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
        ("Ruta 2", "561", None),
        ("Calle San Martín", "789", "3D"),
        ("Avenida Mayo", "1122", "12A"),
    ]
    for addr in addresses:
        address.create_address(*addr)

    # Crear localities
    localities = [
        "La Plata", "San Carlos", "Villa Adelina", "Boulogne", "Martínez", "Beccar",
        "Quilmes", "Avellaneda", "Lanús", "Banfield", "Lomas de Zamora", "Adrogué",
        "Berazategui", "San Fernando", "Tigre", "Vicente López", "Pilar", "Morón", 
        "Hurlingham", "San Isidro", "Escobar", "José C. Paz", "Malvinas Argentinas",
        "San Miguel", "Merlo", "Moreno", "Tres de Febrero", "Ituzaingó", "Ezeiza",
        "Esteban Echeverría", "Florencio Varela", "Almirante Brown", "La Matanza",
        "Tandil", "Olavarría", "Bahía Blanca", "Mar del Plata", "Necochea"
    ]
    for loc in localities:
        locality.create_locality(loc)

    # Provincias de Argentina
    provinces = [
        "Buenos Aires", "Córdoba", "Mendoza", "Santa Fe", "Tucumán",
        "Entre Ríos", "Salta", "Chaco", "Misiones", "San Juan",
        "San Luis", "Jujuy", "Corrientes", "Río Negro", "Neuquén", 
        "Formosa", "La Pampa", "Chubut", "Santa Cruz", "La Rioja",
        "Catamarca", "Santiago del Estero", "Tierra del Fuego"
    ]    
    for prov in provinces:
        province.create_province(prov)

    #############
    # Empleados #
    #############

    # Creado de profesiones
    professions_list = [
        "Psicólogo/a", "Psicomotricista", "Médico/a", "Kinesiólogo/a", "Terapista Ocupacional",
        "Psicopedagogo/a", "Docente", "Profesor", "Fonoaudiólogo/a", "Veterinario/a", "Otro",
        "Fisioterapeuta", "Trabajador/a Social", "Enfermero/a", "Nutricionista",
        "Asistente Social", "Acompañante Terapéutico", "Musicoterapeuta", "Psiquiatra",
        "Neurólogo/a", "Cardiólogo/a"
    ]    
    for prof in professions_list:
        professions.create_profession(prof)

    # Creado de posiciones
    job_positions_list = [
        "Administrativo/a", "Terapeuta", "Conductor", "Auxiliar de pista", "Herrero",
        "Veterinario", "Entrenador de Caballos", "Domador", "Profesor de Equitación", 
        "Docente de Capacitación", "Auxiliar de mantenimiento", "Otro", "Coordinador de Programas",
        "Asistente Administrativo", "Cuidador de Caballos", "Voluntario", "Recepcionista",
        "Mantenimiento", "Psicólogo/a Institucional", "Técnico en Equipos", "Encargado de Seguridad"
    ]    
    for job in job_positions_list:
        job_positions.create_job_position(job)

    # Creado de empleados
    employees = [
        {
            "name": "Juans",
            "surname": "Pérezs",
            "dni": "123456001",
            "address_id": 1,
            "email": "juans.perez@example.com",
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
            "job_position_id": 7,
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
            "job_position_id": 7,
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
       {
            "name": "Esteban",
            "surname": "García",
            "dni": "91234567",
            "address_id": 1,
            "email": "esteban.garcia@example.com",
            "locality_id": 1,
            "phone": "555-0111",
            "profession_id": 1,
            "job_position_id": 1,
            "emergency_contact_name": "Ana García",
            "emergency_contact_phone": "555-9877",
            "obra_social": "Obra Social A",
            "affiliate_number": "A123457",
            "is_volunteer": False,
            "user_id": 11,
            "enabled": True,
            "start_date": datetime(2023, 1, 15),
            "end_date": None
        },
        {
            "name": "Marta",
            "surname": "Jiménez",
            "dni": "82345678",
            "address_id": 2,
            "email": "marta.jimenez@example.com",
            "locality_id": 2,
            "phone": "555-0222",
            "profession_id": 2,
            "job_position_id": 2,
            "emergency_contact_name": "Luis Jiménez",
            "emergency_contact_phone": "555-8766",
            "obra_social": "Obra Social B",
            "affiliate_number": "B234568",
            "is_volunteer": True,
            "user_id": 12,
            "enabled": True,
            "start_date": datetime(2023, 2, 1),
            "end_date": None
        },
        {
            "name": "Hugo",
            "surname": "Soto",
            "dni": "73456789",
            "address_id": 3,
            "email": "hugo.soto@example.com",
            "locality_id": 3,
            "phone": "555-0333",
            "profession_id": 3,
            "job_position_id": 3,
            "emergency_contact_name": "Sofía Soto",
            "emergency_contact_phone": "555-7655",
            "obra_social": "Obra Social C",
            "affiliate_number": "C345679",
            "is_volunteer": False,
            "user_id": 13,
            "enabled": True,
            "start_date": datetime(2023, 3, 10),
            "end_date": None
        },
        {
            "name": "Rocío",
            "surname": "Mendoza",
            "dni": "84567890",
            "address_id": 4,
            "email": "rocio.mendoza@example.com",
            "locality_id": 4,
            "phone": "555-0444",
            "profession_id": 1,
            "job_position_id": 4,
            "emergency_contact_name": "Fernando Mendoza",
            "emergency_contact_phone": "555-6544",
            "obra_social": "Obra Social D",
            "affiliate_number": "D456780",
            "is_volunteer": True,
            "user_id": 14,
            "enabled": True,
            "start_date": datetime(2023, 4, 20),
            "end_date": None
        },
        {
            "name": "Camila",
            "surname": "Torres",
            "dni": "95678901",
            "address_id": 5,
            "email": "camila.torres@example.com",
            "locality_id": 5,
            "phone": "555-0555",
            "profession_id": 2,
            "job_position_id": 5,
            "emergency_contact_name": "Hugo Torres",
            "emergency_contact_phone": "555-5433",
            "obra_social": "Obra Social E",
            "affiliate_number": "E567891",
            "is_volunteer": False,
            "user_id": 15,
            "enabled": True,
            "start_date": datetime(2023, 5, 15),
            "end_date": None
        },
        {
            "name": "Felipe",
            "surname": "Núñez",
            "dni": "06789012",
            "address_id": 6,
            "email": "felipe.nunez@example.com",
            "locality_id": 6,
            "phone": "555-0666",
            "profession_id": 3,
            "job_position_id": 1,
            "emergency_contact_name": "Patricia Núñez",
            "emergency_contact_phone": "555-4322",
            "obra_social": "Obra Social F",
            "affiliate_number": "F678902",
            "is_volunteer": True,
            "user_id": 16,
            "enabled": True,
            "start_date": datetime(2023, 6, 30),
            "end_date": None
        },
        {
            "name": "Adrián",
            "surname": "Salas",
            "dni": "17890123",
            "address_id": 7,
            "email": "adrian.salas@example.com",
            "locality_id": 7,
            "phone": "555-0777",
            "profession_id": 1,
            "job_position_id": 2,
            "emergency_contact_name": "Laura Salas",
            "emergency_contact_phone": "555-3211",
            "obra_social": "Obra Social G",
            "affiliate_number": "G789013",
            "is_volunteer": False,
            "user_id": 17,
            "enabled": True,
            "start_date": datetime(2023, 7, 25),
            "end_date": None
        },
        {
            "name": "Valeria",
            "surname": "López",
            "dni": "28901234",
            "address_id": 8,
            "email": "valeria.lopez@example.com",
            "locality_id": 8,
            "phone": "555-0888",
            "profession_id": 2,
            "job_position_id": 3,
            "emergency_contact_name": "Carlos López",
            "emergency_contact_phone": "555-2108",
            "obra_social": "Obra Social H",
            "affiliate_number": "H890124",
            "is_volunteer": True,
            "user_id": 18,
            "enabled": True,
            "start_date": datetime(2023, 8, 5),
            "end_date": None
        },
        {
            "name": "Roberto",
            "surname": "Rivera",
            "dni": "39012345",
            "address_id": 9,
            "email": "roberto.rivera@example.com",
            "locality_id": 9,
            "phone": "555-0999",
            "profession_id": 3,
            "job_position_id": 4,
            "emergency_contact_name": "Elena Rivera",
            "emergency_contact_phone": "555-1097",
            "obra_social": "Obra Social I",
            "affiliate_number": "I901235",
            "is_volunteer": False,
            "user_id": 19,
            "enabled": True,
            "start_date": datetime(2023, 9, 10),
            "end_date": None
        },
        {
            "name": "Nadia",
            "surname": "Castillo",
            "dni": "40223434",
            "address_id": 10,
            "email": "nadia_castillo@example.com",
            "locality_id": 10,
            "phone": "555-1011",
            "profession_id": 1,
            "job_position_id": 1,
            "emergency_contact_name": "Ricardo Castillo",
            "emergency_contact_phone": "555-2018",
            "obra_social": "Obra Social J",
            "affiliate_number": "J012346",
            "is_volunteer": True,
            "user_id": 20,
            "enabled": True,
            "start_date": datetime(2023, 10, 1),
            "end_date": None
        }
    ]

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


    #############################
    # Riders and horses Section #
    #############################

    # Create disability types
    disability_types_list = ["Mental", "Motora", "Sensorial", "Visceral", "Múltiple"]
    for dt in disability_types_list:
        disability_types.create_disability_type(dt)

    # Create disability diagnoses
    diagnoses_list = [
        "Parálisis Cerebral", "Síndrome de Down", "Autismo", "Lesión Medular", 
        "Esclerosis Múltiple", "Distrofia Muscular", "ECNE", "Lesión post-traumática", 
        "Mielomeningocele", "Escoliosis Leve", "Secuelas de ACV", 
        "Discapacidad Intelectual", "Trastorno del Espectro Autista", 
        "Trastorno del Aprendizaje", "Trastorno por Déficit de Atención/Hiperactividad", 
        "Trastorno de la Comunicación", "Trastorno de Ansiedad", "Retraso Madurativo", 
        "Psicosis", "Trastorno de Conducta", "Trastornos del ánimo y afectivos", 
        "Trastorno Alimentario", "OTRO"
    ]
    for diag in diagnoses_list:
        disability_diagnoses.create_disability_diagnosis(diag)

    # Create sedes
    sedes_list = ["Sede Central", "Sede Norte", "Sede Sur", "Sede Este", "Sede Oeste"]
    for sede in sedes_list:
        sedes.create_sede(sede)

    # Create work proposals
    proposals = ["Hipoterapia", "Monta Terapéutica", "Equitación Adaptada", "Volteo Adaptado", "Carruaje Adaptado", "Deporte Ecuestre Adaptado", "Actividades Recreativas"]
    for prop in proposals:
        work_proposals.create_work_proposal(prop)

    # Create horses

    horses.create_horse(name="Trueno", birth=datetime(2015, 6, 1), sex=True, breed="Árabe", coat="Bayo", is_donated=False, sede_id=1, active=True, activity_id=1)
    horses.create_horse(name="Relámpago", birth=datetime(2017, 3, 15), sex=True, breed="Pura Sangre", coat="Alazán", is_donated=True, sede_id=2, active=True, activity_id=2)
    horses.create_horse(name="Tormenta", birth=datetime(2016, 9, 25), sex=False, breed="Appaloosa", coat="Negro", is_donated=False, sede_id=4, active=True, activity_id=3)
    horses.create_horse(name="Fuego", birth=datetime(2014, 12, 5), sex=False, breed="Quarter Horse", coat="Dorado", is_donated=True, sede_id=3, active=True, activity_id=4)
    horses.create_horse(name="Sombra", birth=datetime(2013, 7, 11), sex=False, breed="Mustang", coat="Gris", is_donated=False, sede_id=2, active=True, activity_id=5)
    horses.create_horse(name="Espíritu", birth=datetime(2018, 5, 21), sex=False, breed="Morgan", coat="Palomino", is_donated=True, sede_id=1, active=True, activity_id=1)
    horses.create_horse(name="Místico", birth=datetime(2019, 2, 18), sex=True, breed="Frisón", coat="Negro", is_donated=False, sede_id=3, active=True, activity_id=2)
    horses.create_horse(name="Cometa", birth=datetime(2020, 8, 10), sex=True, breed="Hanoveriano", coat="Castaño", is_donated=True, sede_id=4, active=True, activity_id=3)
    horses.create_horse(name="Margarita", birth=datetime(2015, 11, 30), sex=False, breed="Poni Galés", coat="Bayo", is_donated=False, sede_id=1, active=True, activity_id=4)
    horses.create_horse(name="Jack", birth=datetime(2016, 4, 22), sex=False, breed="Clydesdale", coat="Alazán", is_donated=True, sede_id=3, active=True, activity_id=5)
    horses.create_horse(name="Rubí", birth=datetime(2018, 1, 9), sex=True, breed="Poni Shetland", coat="Negro", is_donated=False, sede_id=2, active=True, activity_id=1)
    horses.create_horse(name="Ahumado", birth=datetime(2017, 10, 16), sex=True, breed="Percherón", coat="Gris", is_donated=True, sede_id=4, active=True, activity_id=2)
    horses.create_horse(name="Tornado", birth=datetime(2014, 6, 29), sex=False, breed="Belga", coat="Dorado", is_donated=False, sede_id=3, active=True, activity_id=3)
    horses.create_horse(name="Aurora", birth=datetime(2019, 8, 7), sex=True, breed="Connemara", coat="Palomino", is_donated=True, sede_id=2, active=True, activity_id=4)
    horses.create_horse(name="Estrella", birth=datetime(2020, 12, 3), sex=True, breed="Islandés", coat="Castaño", is_donated=False, sede_id=1, active=True, activity_id=5)

    # Create work days
    days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
    for day in days:
        work_days.create_work_day(day)

    # Create family allowance types
    allowance_types = ["Asignacion Universal por Hijo", "Asignacion Universal por hijo con Discapacidad", "Asignacion por ayuda escolar anual"]
    for at in allowance_types:
        family_allowance_types.create_family_allowance_type(at)

    # Create pension types
    pension_types_list = ["Nacional", "Provincial"]
    for pt in pension_types_list:
        pension_types.create_pension_type(pt)

    # Create schools
    
# Crear escuelas en Buenos Aires
    schools.create_school(name="Colegio Nacional de Buenos Aires", address="Bolívar 263, CABA", phone="011-4307-1234", observations="Enfocado en formación académica de alto nivel.")
    schools.create_school(name="Escuela Técnica ORT", address="Yatay 240, CABA", phone="011-4857-4567", observations="Reconocida por sus programas en tecnología e innovación.")
    schools.create_school(name="Instituto River Plate", address="Av. Figueroa Alcorta 7597, CABA", phone="011-4789-7890", observations="Fuerte enfoque en educación deportiva y académica.")
    schools.create_school(name="Escuela Superior de Comercio Carlos Pellegrini", address="Marcelo T. de Alvear 1851, CABA", phone="011-4373-6789", observations="Especializada en administración y economía.")
    schools.create_school(name="Escuela Normal Superior en Lenguas Vivas", address="Carlos Pellegrini 1515, CABA", phone="011-4811-5678", observations="Conocida por sus programas en idiomas y traducción.")
    schools.create_school(name="Instituto Libre de Segunda Enseñanza (ILSE)", address="Av. Paseo Colón 1252, CABA", phone="011-4362-8901", observations="Enfocado en ciencias sociales y humanísticas.")
    schools.create_school(name="Colegio San José", address="Bartolomé Mitre 2455, CABA", phone="011-4951-2345", observations="Enfasis en formación religiosa y académica integral.")
    schools.create_school(name="Colegio Nuestra Señora de la Misericordia", address="Perú 435, CABA", phone="011-4331-9012", observations="Excelencia en educación bilingüe y valores cristianos.")
    schools.create_school(name="Colegio Marín", address="Av. del Libertador 17115, San Isidro", phone="011-4747-3456", observations="Enfocado en liderazgo y desarrollo personal.")
    schools.create_school(name="Colegio del Pilar", address="Maipú 956, CABA", phone="011-4312-6789", observations="Fuerte énfasis en educación en ciencias y humanidades.")
    schools.create_school(name="Colegio Belgrano Day School", address="Juramento 1931, CABA", phone="011-4783-3456", observations="Destacado por su educación bilingüe y currículo internacional.")
    schools.create_school(name="Instituto French", address="Moreno 1576, San Fernando", phone="011-4745-6789", observations="Ofrece educación integral con orientación humanística.")
    schools.create_school(name="Instituto María Auxiliadora", address="Av. Pueyrredón 751, CABA", phone="011-4961-1234", observations="Conocido por su educación en valores y desarrollo integral.")
    schools.create_school(name="Escuela Cristiana Evangélica Argentina", address="Coronel Díaz 2942, CABA", phone="011-4823-2345", observations="Enseñanza basada en valores cristianos.")
    schools.create_school(name="Instituto La Salle", address="Hipólito Yrigoyen 4254, CABA", phone="011-4952-9012", observations="Famoso por su formación técnica y en valores.")
    schools.create_school(name="Escuela Técnica Raggio", address="Av. del Libertador 8651, CABA", phone="011-4701-7890", observations="Enfasis en formación técnica en ciencias aplicadas.")
    schools.create_school(name="Escuela de Comercio Nº 7", address="Juncal 1287, CABA", phone="011-4815-6789", observations="Destacada en ciencias económicas y administrativas.")
    schools.create_school(name="Colegio Champagnat", address="Marcelo T. de Alvear 1600, CABA", phone="011-4816-3456", observations="Fuerte enfoque en educación humanística y social.")
    schools.create_school(name="Instituto San Antonio de Padua", address="Av. San Martín 3030, CABA", phone="011-4581-5678", observations="Destacado por su orientación en artes y ciencias sociales.")
    schools.create_school(name="Escuela Argentina Modelo", address="Aráoz 2800, CABA", phone="011-4861-2345", observations="Reconocida por su currículo en ciencias y arte.")
    schools.create_school(name="Escuela Técnica N°5", address="Av. Álvarez Jonte 4950, CABA", phone="011-4561-7890", observations="Destacada en formación técnica y científica.")
    schools.create_school(name="Instituto Santa Ana", address="Calle 9 de Julio 1234, Tigre", phone="011-4749-3456", observations="Enseñanza en valores cristianos y educación bilingüe.")
    schools.create_school(name="Colegio Santa Isabel", address="Av. de Mayo 2564, Moreno", phone="011-4623-5678", observations="Conocido por su enfoque en humanidades y ciencias.")
    schools.create_school(name="Colegio Los Robles", address="Paraná 2245, San Isidro", phone="011-4737-9012", observations="Enseñanza personalizada y orientación académica sólida.")
    schools.create_school(name="Instituto Grilli", address="Av. Maipú 2200, Vicente López", phone="011-4795-6789", observations="Educación bilingüe y enfoque en liderazgo.")
    schools.create_school(name="Colegio Nacional Rafael Hernández", address="Av. 1 e/ 47 y 48, La Plata", phone="0221-425-1234", observations="Colegio público con excelencia académica.")
    schools.create_school(name="Escuela Graduada Joaquín V. González", address="Calle 50 e/ 117 y 118, La Plata", phone="0221-427-5678", observations="Enfocada en formación integral y humanística.")
    schools.create_school(name="Colegio Nuestra Señora de Lourdes", address="Calle 3 e/ 62 y 63, La Plata", phone="0221-482-7890", observations="Colegio católico con enseñanza en valores.")
    schools.create_school(name="Instituto Inmaculada", address="Calle 44 e/ 5 y 6, La Plata", phone="0221-424-9012", observations="Reconocido por su educación bilingüe y compromiso social.")
    schools.create_school(name="Colegio San Luis", address="Calle 9 e/ 57 y 58, La Plata", phone="0221-421-3456", observations="Colegio mixto con formación académica sólida.")
    schools.create_school(name="Instituto Mater Dei", address="Calle 13 e/ 64 y 65, La Plata", phone="0221-427-6789", observations="Especializado en educación cristiana y humanística.")
    schools.create_school(name="Escuela Técnica Nº 2 Albert Thomas", address="Calle 1 e/ 57 y 58, La Plata", phone="0221-482-2345", observations="Escuela técnica destacada en formación industrial y técnica.")
    schools.create_school(name="Instituto Superior de Formación Docente Nº 9", address="Calle 59 e/ 8 y 9, La Plata", phone="0221-483-5678", observations="Formación de docentes con especialización en pedagogía.")
    schools.create_school(name="Colegio Sagrado Corazón", address="Calle 12 e/ 39 y 40, La Plata", phone="0221-421-7890", observations="Colegio católico con énfasis en educación moral.")
    schools.create_school(name="Escuela de Enseñanza Técnica Nº 3", address="Calle 52 e/ 3 y 4, La Plata", phone="0221-425-9012", observations="Ofrece especialidades en electromecánica y electrónica.")
    schools.create_school(name="Colegio San Cayetano", address="Calle 6 e/ 46 y 47, La Plata", phone="0221-423-3456", observations="Con fuerte enfoque en educación en valores y deportes.")
    schools.create_school(name="Instituto Superior Juan N. Terranova", address="Calle 54 e/ 7 y 8, La Plata", phone="0221-429-6789", observations="Especializado en formación técnica y profesional.")
    schools.create_school(name="Colegio Patris", address="Calle 8 e/ 36 y 37, La Plata", phone="0221-426-2345", observations="Conocido por su formación en ciencias y humanidades.")
    schools.create_school(name="Escuela Normal Nº 1 Mary O. Graham", address="Calle 51 e/ 14 y 15, La Plata", phone="0221-421-5678", observations="Reconocida por su formación en ciencias de la educación.")
    schools.create_school(name="Colegio Santa Teresa de Jesús", address="Calle 5 e/ 42 y 43, La Plata", phone="0221-428-7890", observations="Colegio religioso con orientación humanística.")
    schools.create_school(name="Escuela Técnica Nº 5", address="Calle 7 e/ 76 y 77, La Plata", phone="0221-427-9012", observations="Formación en tecnología aplicada y electrónica.")
    schools.create_school(name="Instituto San Vicente de Paul", address="Calle 60 e/ 10 y 11, La Plata", phone="0221-424-3456", observations="Enseñanza católica con fuerte orientación social.")
    schools.create_school(name="Escuela Secundaria Técnica Nº 4", address="Calle 1 e/ 68 y 69, La Plata", phone="0221-429-6789", observations="Destacada por su formación en mecánica y construcción.")
    schools.create_school(name="Colegio Lincoln", address="Calle 11 e/ 34 y 35, La Plata", phone="0221-423-2345", observations="Educación bilingüe y enfoque en ciencias y artes.")
    schools.create_school(name="Instituto Cultural Argentino", address="Calle 55 e/ 8 y 9, La Plata", phone="0221-481-5678", observations="Enseñanza personalizada con foco en la cultura y el arte.")
    schools.create_school(name="Colegio Virgen del Pilar", address="Calle 61 e/ 10 y 11, La Plata", phone="0221-486-7890", observations="Educación cristiana y fuerte compromiso social.")
    schools.create_school(name="Instituto El Carmen", address="Calle 9 e/ 38 y 39, La Plata", phone="0221-422-9012", observations="Enseñanza en valores y orientación religiosa.")
    schools.create_school(name="Colegio San Pio X", address="Calle 58 e/ 8 y 9, La Plata", phone="0221-480-3456", observations="Fuerte en educación técnica y en ciencias aplicadas.")
    schools.create_school(name="Escuela Nuestra Señora de la Paz", address="Calle 16 e/ 46 y 47, La Plata", phone="0221-427-6789", observations="Orientación cristiana y formación académica.")
    schools.create_school(name="Colegio Santa Ana", address="Calle 6 e/ 67 y 68, La Plata", phone="0221-483-2345", observations="Enseñanza personalizada con orientación en ciencias.")
    schools.create_school(name="Instituto Domingo Savio", address="Calle 33 e/ 10 y 11, La Plata", phone="0221-481-5678", observations="Educación en valores y formación católica.")
    schools.create_school(name="Escuela de Comercio N° 32", address="Calle 19 e/ 45 y 46, La Plata", phone="0221-420-7890", observations="Enfocado en administración y ciencias contables.")
    schools.create_school(name="Colegio Santa Lucía", address="Calle 15 e/ 50 y 51, La Plata", phone="0221-422-9012", observations="Formación cristiana y programas de voluntariado.")
    schools.create_school(name="Instituto San Jorge", address="Calle 31 e/ 9 y 10, La Plata", phone="0221-425-3456", observations="Colegio mixto con orientación en ciencias y arte.")
    schools.create_school(name="Colegio Pablo VI", address="Calle 30 e/ 8 y 9, La Plata", phone="0221-421-6789", observations="Enseñanza religiosa con enfoque en desarrollo humano.")
    schools.create_school(name="Instituto Santa María", address="Calle 2 e/ 41 y 42, La Plata", phone="0221-429-2345", observations="Conocido por su educación bilingüe y actividades artísticas.")

    from datetime import date
    # Create riders
    riders.create_rider(
        name="Emma", last_name="Lopez", dni="22334455", age=26, birth_date=date(1998, 4, 18),
        birth_locality_id=8, birth_province_id=9, address_id=8, current_locality_id=9,
        current_province_id=10, phone="555-7777", emergency_contact_name="David Lopez",
        emergency_contact_phone="555-8888", active=True, sede_id=4, has_scholarship=False,
        scholarship_percentage=None, has_disability_certificate=True, disability_diagnosis_id=4,
        disability_type_id=2, receives_family_allowance=True, family_allowance_type_id=3,
        receives_pension=True, pension_type_id=2, health_insurance="BlueCare",
        affiliate_number="BC98765", has_guardianship=True, school_id=3, current_grade="Grade 5",
        attending_professionals="Dr. Purple", work_proposal_id=4, teacher_id=8,
        horse_conductor_id=9, horse_id=8, track_assistant_id=5,
        guardian1_name="John", guardian1_last_name="Doe", guardian1_dni="12345678",
        guardian1_address_id=10, guardian1_locality_id=5, guardian1_province_id=6,
        guardian1_phone="555-9999", guardian1_email="john.doe@example.com",
        guardian1_education_level="College", guardian1_occupation="Engineer",
        guardian1_relationship="Father", guardian2_name="Jane", guardian2_last_name="Doe",
        guardian2_dni="87654321", guardian2_address_id=4, guardian2_locality_id=2,
        guardian2_province_id=5, guardian2_phone="555-8888", guardian2_email="jane.doe@example.com",
        guardian2_education_level="High School", guardian2_occupation="Teacher",
        guardian2_relationship="Mother"
    )

    riders.create_rider(
        name="Liam", last_name="Smith", dni="33445566", age=27, birth_date=date(1997, 5, 19),
        birth_locality_id=9, birth_province_id=5, address_id=9, current_locality_id=10,
        current_province_id=2, phone="555-7778", emergency_contact_name="Michael Smith",
        emergency_contact_phone="555-8889", active=True, sede_id=5, has_scholarship=True,
        scholarship_percentage=50, has_disability_certificate=False, disability_diagnosis_id=None,
        disability_type_id=3, receives_family_allowance=False, family_allowance_type_id=None,
        receives_pension=False, pension_type_id=None, health_insurance="RedCare",
        affiliate_number="RC87654", has_guardianship=True, school_id=5, current_grade="Grade 6",
        attending_professionals="Dr. Green", work_proposal_id=5, teacher_id=9,
        horse_conductor_id=10, horse_id=9, track_assistant_id=3,
        guardian1_name="Kevin", guardian1_last_name="Smith", guardian1_dni="23456789",
        guardian1_address_id=2, guardian1_locality_id=4, guardian1_province_id=7,
        guardian1_phone="555-1111", guardian1_email="kevin.smith@example.com",
        guardian1_education_level="Bachelor", guardian1_occupation="Doctor",
        guardian1_relationship="Father", guardian2_name="Laura", guardian2_last_name="Smith",
        guardian2_dni="98765432", guardian2_address_id=5, guardian2_locality_id=2,
        guardian2_province_id=6, guardian2_phone="555-2222", guardian2_email="laura.smith@example.com",
        guardian2_education_level="Diploma", guardian2_occupation="Nurse",
        guardian2_relationship="Mother"
    )

    riders.create_rider(
        name="Sofia", last_name="Perez", dni="11223344", age=25, birth_date=date(1999, 1, 22),
        birth_locality_id=2, birth_province_id=3, address_id=4, current_locality_id=5,
        current_province_id=6, phone="555-1111", emergency_contact_name="Maria Perez",
        emergency_contact_phone="555-2222", active=True, sede_id=1, has_scholarship=True,
        scholarship_percentage=75, has_disability_certificate=False, disability_diagnosis_id=None,
        disability_type_id=2, receives_family_allowance=True, family_allowance_type_id=1,
        receives_pension=False, pension_type_id=None, health_insurance="GreenCare",
        affiliate_number="GC12345", has_guardianship=True, school_id=1, current_grade="Grade 3",
        attending_professionals="Dr. Blue", work_proposal_id=2, teacher_id=1,
        horse_conductor_id=2, horse_id=1, track_assistant_id=2,
        guardian1_name="Carlos", guardian1_last_name="Perez", guardian1_dni="45678912",
        guardian1_address_id=2, guardian1_locality_id=3, guardian1_province_id=4,
        guardian1_phone="555-3333", guardian1_email="carlos.perez@example.com",
        guardian1_education_level="Masters", guardian1_occupation="Architect",
        guardian1_relationship="Father", guardian2_name="Ana", guardian2_last_name="Perez",
        guardian2_dni="65432198", guardian2_address_id=5, guardian2_locality_id=6,
        guardian2_province_id=7, guardian2_phone="555-4444", guardian2_email="ana.perez@example.com",
        guardian2_education_level="Bachelors", guardian2_occupation="Lawyer",
        guardian2_relationship="Mother"
    )

    riders.create_rider(
        name="Mateo", last_name="Garcia", dni="22335577", age=24, birth_date=date(2000, 3, 15),
        birth_locality_id=7, birth_province_id=8, address_id=6, current_locality_id=7,
        current_province_id=8, phone="555-5555", emergency_contact_name="Laura Garcia",
        emergency_contact_phone="555-6666", active=True, sede_id=3, has_scholarship=False,
        scholarship_percentage=None, has_disability_certificate=True, disability_diagnosis_id=3,
        disability_type_id=1, receives_family_allowance=True, family_allowance_type_id=2,
        receives_pension=True, pension_type_id=1, health_insurance="YellowCare",
        affiliate_number="YC65432", has_guardianship=True, school_id=4, current_grade="Grade 4",
        attending_professionals="Dr. Orange", work_proposal_id=3, teacher_id=4,
        horse_conductor_id=3, horse_id=4, track_assistant_id=3,
        guardian1_name="Jose", guardian1_last_name="Garcia", guardian1_dni="98765432",
        guardian1_address_id=7, guardian1_locality_id=8, guardian1_province_id=9,
        guardian1_phone="555-7777", guardian1_email="jose.garcia@example.com",
        guardian1_education_level="Doctorate", guardian1_occupation="Professor",
        guardian1_relationship="Father", guardian2_name="Maria", guardian2_last_name="Garcia",
        guardian2_dni="87654321", guardian2_address_id=8, guardian2_locality_id=9,
        guardian2_province_id=1, guardian2_phone="555-8888", guardian2_email="maria.garcia@example.com",
        guardian2_education_level="Masters", guardian2_occupation="Researcher",
        guardian2_relationship="Mother"
    )

    riders.create_rider(
        name="Valentina", last_name="Martinez", dni="33447788", age=23, birth_date=date(2001, 2, 10),
        birth_locality_id=4, birth_province_id=5, address_id=3, current_locality_id=4,
        current_province_id=5, phone="555-9999", emergency_contact_name="Pedro Martinez",
        emergency_contact_phone="555-0000", active=True, sede_id=2, has_scholarship=True,
        scholarship_percentage=100, has_disability_certificate=True, disability_diagnosis_id=5,
        disability_type_id=3, receives_family_allowance=False, family_allowance_type_id=None,
        receives_pension=True, pension_type_id=2, health_insurance="OrangeCare",
        affiliate_number="OC87654", has_guardianship=True, school_id=3, current_grade="Grade 2",
        attending_professionals="Dr. Red", work_proposal_id=1, teacher_id=2,
        horse_conductor_id=1, horse_id=2, track_assistant_id=1,
        guardian1_name="Ricardo", guardian1_last_name="Martinez", guardian1_dni="56789012",
        guardian1_address_id=4, guardian1_locality_id=5, guardian1_province_id=6,
        guardian1_phone="555-1111", guardian1_email="ricardo.martinez@example.com",
        guardian1_education_level="College", guardian1_occupation="Engineer",
        guardian1_relationship="Father", guardian2_name="Luisa", guardian2_last_name="Martinez",
        guardian2_dni="78901234", guardian2_address_id=6, guardian2_locality_id=7,
        guardian2_province_id=8, guardian2_phone="555-2222", guardian2_email="luisa.martinez@example.com",
        guardian2_education_level="High School", guardian2_occupation="Teacher",
        guardian2_relationship="Mother"
    )

    riders.create_rider(
        name="Lucas", last_name="Rodriguez", dni="44556677", age=28, birth_date=date(1996, 9, 25),
        birth_locality_id=6, birth_province_id=7, address_id=5, current_locality_id=6,
        current_province_id=7, phone="555-3333", emergency_contact_name="Marcela Rodriguez",
        emergency_contact_phone="555-4444", active=True, sede_id=2, has_scholarship=False,
        scholarship_percentage=None, has_disability_certificate=True, disability_diagnosis_id=6,
        disability_type_id=2, receives_family_allowance=True, family_allowance_type_id=2,
        receives_pension=False, pension_type_id=None, health_insurance="PinkCare",
        affiliate_number="PC12345", has_guardianship=True, school_id=5, current_grade="Grade 1",
        attending_professionals="Dr. Yellow", work_proposal_id=3, teacher_id=5,
        horse_conductor_id=6, horse_id=5, track_assistant_id=6,
        guardian1_name="Hector", guardian1_last_name="Rodriguez", guardian1_dni="34567890",
        guardian1_address_id=9, guardian1_locality_id=10, guardian1_province_id=5,
        guardian1_phone="555-5555", guardian1_email="hector.rodriguez@example.com",
        guardian1_education_level="Masters", guardian1_occupation="Architect",
        guardian1_relationship="Father", guardian2_name="Silvia", guardian2_last_name="Rodriguez",
        guardian2_dni="12345678", guardian2_address_id=7, guardian2_locality_id=8,
        guardian2_province_id=9, guardian2_phone="555-6666", guardian2_email="silvia.rodriguez@example.com",
        guardian2_education_level="Bachelors", guardian2_occupation="Lawyer",
        guardian2_relationship="Mother"
    )

    riders.create_rider(
        name="Martina", last_name="Fernandez", dni="55667788", age=30, birth_date=date(1994, 7, 18),
        birth_locality_id=3, birth_province_id=4, address_id=1, current_locality_id=3,
        current_province_id=4, phone="555-7777", emergency_contact_name="Daniel Fernandez",
        emergency_contact_phone="555-8888", active=True, sede_id=2, has_scholarship=True,
        scholarship_percentage=90, has_disability_certificate=False, disability_diagnosis_id=None,
        disability_type_id=3, receives_family_allowance=True, family_allowance_type_id=1,
        receives_pension=True, pension_type_id=2, health_insurance="GrayCare",
        affiliate_number="GC54321", has_guardianship=True, school_id=2, current_grade="Grade 5",
        attending_professionals="Dr. White", work_proposal_id=2, teacher_id=6,
        horse_conductor_id=7, horse_id=6, track_assistant_id=7,
        guardian1_name="Jorge", guardian1_last_name="Fernandez", guardian1_dni="23456789",
        guardian1_address_id=2, guardian1_locality_id=3, guardian1_province_id=4,
        guardian1_phone="555-9999", guardian1_email="jorge.fernandez@example.com",
        guardian1_education_level="College", guardian1_occupation="Engineer",
        guardian1_relationship="Father", guardian2_name="Silvia", guardian2_last_name="Fernandez",
        guardian2_dni="34567890", guardian2_address_id=3, guardian2_locality_id=4,
        guardian2_province_id=5, guardian2_phone="555-1111", guardian2_email="silvia.fernandez@example.com",
        guardian2_education_level="High School", guardian2_occupation="Teacher",
        guardian2_relationship="Mother"
    )

    riders.create_rider(
        name="Lucas", last_name="Alvarez", dni="66778899", age=22, birth_date=date(2002, 6, 30),
        birth_locality_id=2, birth_province_id=3, address_id=3, current_locality_id=4,
        current_province_id=5, phone="555-2222", emergency_contact_name="Paula Alvarez",
        emergency_contact_phone="555-3333", active=True, sede_id=4, has_scholarship=False,
        scholarship_percentage=None, has_disability_certificate=True, disability_diagnosis_id=2,
        disability_type_id=1, receives_family_allowance=True, family_allowance_type_id=2,
        receives_pension=False, pension_type_id=None, health_insurance="BlueShield",
        affiliate_number="BS12345", has_guardianship=True, school_id=3, current_grade="Grade 6",
        attending_professionals="Dr. Green", work_proposal_id=5, teacher_id=8,
        horse_conductor_id=9, horse_id=7, track_assistant_id=8,
        guardian1_name="Miguel", guardian1_last_name="Alvarez", guardian1_dni="98765432",
        guardian1_address_id=9, guardian1_locality_id=10, guardian1_province_id=2,
        guardian1_phone="555-4444", guardian1_email="miguel.alvarez@example.com",
        guardian1_education_level="Masters", guardian1_occupation="Doctor",
        guardian1_relationship="Father", guardian2_name="Claudia", guardian2_last_name="Alvarez",
        guardian2_dni="87654321", guardian2_address_id=10, guardian2_locality_id=1,
        guardian2_province_id=4, guardian2_phone="555-5555", guardian2_email="claudia.alvarez@example.com",
        guardian2_education_level="Bachelors", guardian2_occupation="Nurse",
        guardian2_relationship="Mother"
    )

    riders.create_rider(
        name="Camila", last_name="Lopez", dni="77889900", age=21, birth_date=date(2003, 10, 10),
        birth_locality_id=8, birth_province_id=9, address_id=2, current_locality_id=5,
        current_province_id=2, phone="555-6666", emergency_contact_name="Sofia Lopez",
        emergency_contact_phone="555-7777", active=True, sede_id=2, has_scholarship=False,
        scholarship_percentage=None, has_disability_certificate=False, disability_diagnosis_id=None,
        disability_type_id=2, receives_family_allowance=False, family_allowance_type_id=None,
        receives_pension=True, pension_type_id=1, health_insurance="HealthCare",
        affiliate_number="HC87654", has_guardianship=True, school_id=1, current_grade="Grade 1",
        attending_professionals="Dr. Pink", work_proposal_id=3, teacher_id=2,
        horse_conductor_id=1, horse_id=3, track_assistant_id=1,
        guardian1_name="Juan", guardian1_last_name="Lopez", guardian1_dni="22334455",
        guardian1_address_id=2, guardian1_locality_id=3, guardian1_province_id=4,
        guardian1_phone="555-8888", guardian1_email="juan.lopez@example.com",
        guardian1_education_level="College", guardian1_occupation="Engineer",
        guardian1_relationship="Father", guardian2_name="Lucia", guardian2_last_name="Lopez",
        guardian2_dni="99887766", guardian2_address_id=3, guardian2_locality_id=4,
        guardian2_province_id=5, guardian2_phone="555-9999", guardian2_email="lucia.lopez@example.com",
        guardian2_education_level="High School", guardian2_occupation="Teacher",
        guardian2_relationship="Mother"
    )

    

    ##############################
    # REGISTRO DE PAGOS Y COBROS #
    ##############################

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
        (5600, datetime(2024, 10, 20), "Pago de servicios", 3, 2),
        (900, datetime(2024, 8, 25), "Mantenimiento de equipos", 2, None),
        (11500, datetime(2024, 9, 3), "Renovación de contrato", 4, 5),
        (2200, datetime(2023, 12, 30), "Pago parcial", 5, 1),
        (3600, datetime(2022, 7, 15), "Compra de suministros", 2, 3),
        (8900, datetime(2023, 2, 11), "Donación puntual", 1, None),
        (4500, datetime(2024, 1, 20), "Honorarios de consultoría", 3, 4),
        (6800, datetime(2023, 6, 25), "Pago de impuestos", 5, 6),
        (9700, datetime(2024, 8, 1), "Pago de publicidad", 2, None),
        (2300, datetime(2023, 5, 14), "Compra de mobiliario", 4, 3),
        (19000, datetime(2023, 9, 17), "Gastos generales", 1, None),
        (7500, datetime(2024, 3, 9), "Renovación de equipos", 5, 5),
        (4100, datetime(2022, 11, 4), "Pago de electricidad", 3, 1),
        (3200, datetime(2024, 7, 22), "Arreglo de infraestructura", 2, 4),
        (6200, datetime(2024, 4, 18), "Pago de evento especial", 4, 6),
        (5700, datetime(2023, 10, 6), "Material de oficina", 1, 3),
        (4300, datetime(2024, 5, 26), "Compra de tecnología", 3, 2),
        (8900, datetime(2023, 3, 3), "Pago adicional", 5, 4),
        (4800, datetime(2023, 8, 11), "Pago de reparaciones", 2, None),
        (16000, datetime(2024, 6, 30), "Renovación de licencia", 1, 5),
        (2100, datetime(2022, 10, 19), "Mantenimiento de software", 4, None),
        (5900, datetime(2024, 2, 5), "Pago por diseño gráfico", 3, 6),
        (7100, datetime(2023, 12, 17), "Inversión en capacitación", 5, 1),
        (3700, datetime(2023, 7, 13), "Pago de consultoría", 1, 2),
        (8100, datetime(2024, 3, 21), "Compra de uniformes", 4, 4),
        (2700, datetime(2024, 8, 7), "Servicios de limpieza", 2, 3),
        (5600, datetime(2023, 9, 15), "Pago de hosting", 3, 5),
        (8500, datetime(2022, 4, 28), "Pago de dominio", 5, None),
        (2900, datetime(2024, 10, 10), "Gastos de transporte", 2, 1),
        (9300, datetime(2023, 11, 16), "Pago de marketing digital", 1, 6),
        (3900, datetime(2022, 6, 22), "Compra de herramientas", 4, 2),
        (6400, datetime(2023, 5, 8), "Insumos médicos", 3, None),
        (4700, datetime(2024, 7, 29), "Material educativo", 5, 4),
        (1200, datetime(2023, 3, 19), "Pago de conferencia", 1, 3),
        (6000, datetime(2024, 9, 5), "Pago de software", 4, 5),
    ]
    for payment in payments_data:
        payments.create_payment(*payment)

    collection_mediums = ["Efectivo", "Tarjeta de crédito", "Tarjeta de débito", "Transferencia"]
    for cm in collection_mediums:
        collection_medium.create_collection_medium(cm)

    collections_data = [
        (5000, datetime(2024, 9, 10), "Pago realizado en efectivo por servicio", 1, 1, 1),
        (12500, datetime(2024, 9, 12), "Pago por materiales", 2, 2, 2),
        (7200, datetime(2024, 10, 2), "Pago mensual de la membresía", 3, 3, 2),
        (3200, datetime(2024, 10, 5), "Pago parcial por productos", 1, 2, 3),
        (10500, datetime(2024, 10, 6), "Pago total del contrato", 2, 1, 4),
        (4600, datetime(2024, 10, 10), "Donación anual", 1, 4, 6),
        (2850, datetime(2024, 10, 12), "Pago por suscripción", 3, 2, 1),
        (9750, datetime(2024, 10, 15), "Pago por servicios contratados", 2, 3, 4),
        (500, datetime(2024, 10, 18), "Pago parcial por artículo", 1, 1, 3),
        (6900, datetime(2024, 10, 20), "Pago por evento", 2, 4, 5),
        (3700, datetime(2023, 8, 5), "Pago único por servicio", 3, 1, 6),
        (1500, datetime(2024, 1, 17), "Pago por consultas adicionales", 1, 3, 1),
        (8800, datetime(2023, 12, 22), "Pago de productos importados", 2, 4, 3),
        (5400, datetime(2024, 3, 10), "Cobro de gastos médicos", 3, 2, 2),
        (4300, datetime(2024, 2, 5), "Pago por renovación de membresía", 1, 1, 5),
        (3000, datetime(2024, 4, 15), "Cobro de contrato mensual", 2, 3, 6),
        (7600, datetime(2023, 6, 30), "Pago por publicidad", 3, 4, 4),
        (4100, datetime(2024, 9, 8), "Cobro por servicios de asesoría", 1, 2, 3),
        (6500, datetime(2024, 8, 23), "Pago por bienes adquiridos", 2, 3, 1),
        (2300, datetime(2024, 5, 25), "Pago por derechos de uso", 3, 1, 2),
        (4900, datetime(2024, 6, 13), "Pago de seguros", 1, 4, 5),
        (1100, datetime(2024, 7, 11), "Pago único por eventos", 2, 2, 3),
        (3500, datetime(2023, 8, 18), "Pago por licencia anual", 3, 1, 4),
        (9100, datetime(2023, 5, 5), "Pago único por equipamiento", 1, 3, 6),
        (6700, datetime(2024, 4, 19), "Cobro de suscripción premium", 2, 2, 4),
        (5200, datetime(2024, 3, 28), "Pago por mantenimiento", 3, 4, 2),
        (2800, datetime(2023, 9, 14), "Cobro por cuota de inscripción", 1, 3, 5),
        (6300, datetime(2024, 10, 8), "Cobro por servicios adicionales", 2, 1, 6),
        (4600, datetime(2024, 2, 22), "Cobro por equipamiento", 3, 2, 3),
    ]

    # Example of creating these payments and populating the database:
    for collection in collections_data:
        collections.create_collection(*collection)

    document_types_data = ["Entrevista", "Evaluación", "Planificaciones", "Evolución", "Crónicas", "Documental"]

    for dt in document_types_data:
        document_types.create_document_type(dt)
