import datetime
import sqlalchemy
from db_session import SqlAlchemyBase
#  Генерация Базы Данных с использованием ORM и взаимодействие с ней


class FAQ(SqlAlchemyBase):
    __tablename__ = 'faq'

    id_mfc = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('mfc.id_mfc'), nullable=False)
    id_qu = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    question = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    answer = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class Document(SqlAlchemyBase):
    __tablename__ = 'document'

    id_doc = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class Applicant(SqlAlchemyBase):
    __tablename__ = 'applicant'

    id_app = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'),  primary_key=True)
    chat_id = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)  # можно установить id чата
    photo = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=True)
    verified = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)


class Service_Mfc(SqlAlchemyBase):
    __tablename__ = 'service_mfc'

    id_reg = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('registration.id_reg'), primary_key=True)
    id_mfc = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('mfc.id_mfc'), primary_key=True)


class Applicant_Service(SqlAlchemyBase):
    __tablename__ = 'applicant_service'

    id_app = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('applicant.id_app'), primary_key=True)
    id_reg = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('registration.id_reg'), primary_key=True)


class MFC(SqlAlchemyBase):
    __tablename__ = 'mfc'

    id_mfc = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    province = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    geo_coord = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    site_ref = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    social_ref = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class New(SqlAlchemyBase):
    __tablename__ = 'new'

    id_new = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_mfc = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('mfc.id_mfc'), nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    date_publ = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    relevance = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    source = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class Person(SqlAlchemyBase):
    __tablename__ = 'person'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    second_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    first_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    passport = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    gender = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class Registration(SqlAlchemyBase):
    __tablename__ = 'registration'

    id_reg = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date_registration = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    date_admission = sqlalchemy.Column(sqlalchemy.DateTime)
    status = sqlalchemy.Column(sqlalchemy.Boolean, default=True)  # Конечное число состояний заявок
    id_service = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('service.id_service'), nullable=False)


class Employee(SqlAlchemyBase):
    __tablename__ = 'employee'

    id_emp = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'),  primary_key=True)
    department = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    post = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    id_mfc = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('mfc.id_mfc'), nullable=False)


class EmployeeService(SqlAlchemyBase):
    __tablename__ = 'employee_service'

    id_emp = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('employee.id_emp'), primary_key=True)
    id_reg = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('registration.id_reg'), primary_key=True)


class Service(SqlAlchemyBase):
    __tablename__ = 'service'

    id_service = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class ServiceDocument(SqlAlchemyBase):
    __tablename__ = 'service_document'

    id_service = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('service.id_service'), primary_key=True)
    id_doc = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('document.id_doc'), primary_key=True)


class ApplicationMFC(SqlAlchemyBase):
    __tablename__ = 'applicant_mfc'

    id_app = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('applicant.id_app'), primary_key=True)
    id_mfc = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('mfc.id_mfc'), primary_key=True)
