import datetime
import sqlalchemy
from db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'Lusers'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)


class FAQ(SqlAlchemyBase):
    __tablename__ = 'FAQ'

    id_mfc = sqlalchemy.Column()
    id_qu = sqlalchemy.Column()
    question = sqlalchemy.Column()
    answer = sqlalchemy.Column()


class Document(SqlAlchemyBase):
    __tablename__ = 'document'

    id_doc = sqlalchemy.Column()
    name = sqlalchemy.Column()


class Applicant(SqlAlchemyBase):
    __tablename__ = 'applicant'

    id_app = sqlalchemy.Column()
    photo = sqlalchemy.Column()
    verified = sqlalchemy.Column()


class Service_Mfc(SqlAlchemyBase):
    __tablename__ = 'service_mfc'

    id_reg = sqlalchemy.Column()
    id_mfc = sqlalchemy.Column()


class Applicant_Service(SqlAlchemyBase):
    __tablename__ = 'applicant_service'

    id_app = sqlalchemy.Column()
    id_reg = sqlalchemy.Column()


class MFC(SqlAlchemyBase):
    __tablename__ = 'mfc'

    id_mfc = sqlalchemy.Column()
    province = sqlalchemy.Column()
    city = sqlalchemy.Column()
    address = sqlalchemy.Column()
    geo_coord = sqlalchemy.Column()
    site_ref = sqlalchemy.Column()
    social_ref = sqlalchemy.Column()


class New(SqlAlchemyBase):
    __tablename__ = 'new'

    id_new = sqlalchemy.Column()
    id_mfc = sqlalchemy.Column()
    content = sqlalchemy.Column()
    date_publ = sqlalchemy.Column()
    relevance = sqlalchemy.Column()
    source = sqlalchemy.Column()


class Person(SqlAlchemyBase):
    __tablename__ = 'person'

    id = sqlalchemy.Column()
    second_name = sqlalchemy.Column()
    first_name = sqlalchemy.Column()
    passport = sqlalchemy.Column()
    gender = sqlalchemy.Column()


class Registration(SqlAlchemyBase):
    __tablename__ = 'registration'

    id_reg = sqlalchemy.Column()
    date_registration = sqlalchemy.Column()
    date_admission = sqlalchemy.Column()
    status = sqlalchemy.Column()
    id_service = sqlalchemy.Column()


class Employee(SqlAlchemyBase):
    __tablename__ = 'employee'

    id_emp = sqlalchemy.Column()
    department = sqlalchemy.Column()
    post = sqlalchemy.Column()
    id_mfc = sqlalchemy.Column()


class EmployeeService(SqlAlchemyBase):
    __tablename__ = 'employee_service'

    id_emp = sqlalchemy.Column()
    id_reg = sqlalchemy.Column()


class Service(SqlAlchemyBase):
    __tablename__ = 'service'

    id_service = sqlalchemy.Column()
    description = sqlalchemy.Column()


class ServiceDocument(SqlAlchemyBase):
    __tablename__ = 'service_document'

    id_service = sqlalchemy.Column()
    id_doc = sqlalchemy.Column()


class ApplicationMFC(SqlAlchemyBase):
    __tablename__ = 'applicant_mfc'

    id_app = sqlalchemy.Column()
    id_mfc = sqlalchemy.Column()
