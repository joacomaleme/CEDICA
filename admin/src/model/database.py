from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text



db = SQLAlchemy(session_options={'expire_on_commit': False})


def init_app(app):
    """
    Inicializa la base de datos con la aplicacion de Flask.
    """

    db.init_app(app)
    config(app)

    return app


def config(app):
    """
    Configuracion de hooks para la base de datos
    """

    @app.teardown_appcontext
    def close_session(exception=None):
        db.session.close()
    return app


def reset():

    """
    Resetea la base de datos.
    Los imports son NECESARIOS para la funcionalidad.
    Si se agregan nuevas entidades a la bd, debe agregarse el import aca.
    """

    # Probé sin los imports y funciona ¯\(o_o)/¯

    # from src.model.auth.tables.role import Role
    # from src.model.auth.tables.user import User
    # from src.model.auth.tables.permission import Permission
    # from src.model.auth.tables.role_permissions import role_permissions
    # from src.model.employees.tables.employee import Employee
    # from src.model.employees.tables.profession import Profession
    # from src.model.employees.tables.job_position import JobPosition
    # from src.model.riders.tables.rider import Rider
    # from src.model.riders.tables.family_allowance_type import FamilyAllowanceType
    # from src.model.riders.tables.pension_type import PensionType
    # from src.model.riders.tables.disability_type import DisabilityType
    # from src.model.riders.tables.disability_diagnosis import DisabilityDiagnosis
    # from src.model.riders.tables.horse import Horse
    # from src.model.riders.tables.school import School
    # from src.model.riders.tables.guardian import Guardian
    # from src.model.riders.tables.work_day import WorkDay
    # from src.model.riders.tables.rider_work_day import RiderWorkDay
    # from src.model.riders.tables.sede import Sede
    # from src.model.riders.tables.work_proposal import WorkProposal
    # from src.model.generic.tables.address import Address
    # from src.model.generic.tables.document import Document
    # from src.model.generic.tables.locality import Locality
    # from src.model.generic.tables.province import Province
    # from src.model.generic.tables.document_types import DocumentType
    # from src.model.registers.tables.payment import Payment
    # from src.model.registers.tables.payment_type import PaymentType


    print("Eliminando base de datos...")
    # db.session.execute(text('DROP TABLE IF EXISTS users CASCADE;'))
    db.session.commit()
    db.drop_all()  # Drop other tables
    print("Creando base nuevamente...")
    db.create_all()
    print("Done!")
