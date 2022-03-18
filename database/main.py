import db_session
from entity import *
from datetime import datetime, time, date
import pandas as pd
import random


# Глобальная инициализация базы данных, создаются все таблицы, которые необходимо заполнить тут
db_session.global_init("postgre1")
db_sess = db_session.create_session()

# # Регисртрация заявителя
# person = Applicant()
# person.chat_id = "2"
# person.verified = True
# person.second_name = "Artem"
# person.first_name = "Artemchuk"
# person.passport = "1020 2345678"
# person.gender = "M"
# db_sess.add(person)
# db_sess.commit()
#
# # Регистрация МФЦ
# mfc = MFC()
# mfc.province = "Амурская область"
# mfc.city = "Благовещенск"
# mfc.address = "Центральная ул., 37, село Чигири"
# mfc.geo_coord = "127.505075%2C50.339562"
# mfc.site_ref = "https://mfc-amur.ru/"
# mfc.social_ref = "https://vk.com/mfc_russia"
# db_sess.add(mfc)
# db_sess.commit()
#
# mfc = MFC()
# mfc.province = "Амурская область"
# mfc.city = "Благовещенск"
# mfc.address = "ул. 50 лет Октября, 8/2"
# mfc.geo_coord = "127.533494%2C50.260133"
# mfc.site_ref = "https://mfc-amur.ru/"
# mfc.social_ref = "https://vk.com/mfc_russia"
# db_sess.add(mfc)
# db_sess.commit()
#
# Регистрация сотрудника
# employee = Employee()
# employee.department = "Отдел обслуживания"
# employee.post = "Консультант"
# employee.id_mfc = db_sess.query(MFC).filter(MFC.address == "Центральная ул., 37, село Чигири").first().id_mfc
# employee.second_name = "Ara"
# employee.first_name = "Astr"
# employee.passport = "1020 2345678"
# employee.gender = "M"
# db_sess.add(employee)
# db_sess.commit()
#
# # FAQ
# for question, answer in zip(pd.read_csv('../database/FAQ.csv')['question'],
#                             pd.read_csv('../database/FAQ.csv')['answer']):
#     faq = FAQ()
#     faq.answer = answer
#     faq.question = question
#     db_sess.add(faq)
#     db_sess.commit()

# # Сервисы, необходимо
# for q, a, d in zip(pd.read_csv('QAService.csv')['answer1'],
#                        pd.read_csv('QAService.csv')['answer0'], pd.read_csv('QAService.csv')['docs']):
#     ser = Service()
#     ser.description = q + ', ' + a
#     ser.documents = d
#     db_sess.add(ser)
#     db_sess.commit()

# # Заявитель - МФЦ
# app_mfc = ApplicationMFC()
# app_mfc.id_app = db_sess.query(Applicant).filter(Applicant.chat_id == '2').first().id_app
# app_mfc.id_mfc = db_sess.query(MFC).filter(MFC.address == 'ул. 50 лет Октября, 8/2').first().id_mfc
# db_sess.add(app_mfc)
# db_sess.commit()


# print(db_sess.query(MFC).filter(MFC.address == "Центральная ул., 37, село Чигири").first().id_mfc)
# for mfc in db_sess.query(MFC).all():
#     if mfc.address == "Центральная ул., 37, село Чигири":
#         print(mfc.address)

# Регулярка по названию - id service
# id mfc по адрессу
# id чата (наверно)

# mfc = db_sess.query(MFC).filter(MFC.address == "Центральная ул., 37, село Чигири").first().id_mfc
# print(mfc)
# serv = 'Оформление квартиры в собственность'
# service = db_sess.query(Service).filter(Service.description.like(f'%{serv}%')).first().id_service
# print(service)
# # получить регисрации на время в мфц по услуг
# regs = db_sess.query(Registration)\
#     .filter(Registration.date_admission == datetime.combine(date(2022, 7, 14), time(13, 30)))\
#     .filter(Registration.id_mfc == mfc)\
#     .filter(Registration.id_service == service).all()
# # # Если регистрации нет, то давайте сделаем и назначим свободного консультанта
# if not regs:
#     empls = db_sess.query(Registration)\
#         .filter(Registration.date_admission != datetime.combine(date(2022, 7, 14), time(13, 30)))\
#         .filter(Registration.id_mfc == mfc).all()
#     if not empls:
#         # empls = db_sess.query(Employee).all()
#         empls = None
#         print('Нет свободных консультантов')
#     else:
#         empl = random.choice([empl.id_emp for empl in empls])
#         print(empl)
#         # Заполняем заявку дальше
#         # # Регистрация на прием
#         registr = Registration()
#         registr.date_registration = datetime.now()
#         registr.date_admission = datetime.combine(date(2022, 7, 14), time(12, 30))
#         registr.status = True
#         registr.id_service = service
#         registr.id_emp = empl
#         registr.id_mfc = mfc
#         registr.id_app = 1
#         db_sess.add(registr)
#         db_sess.commit()
# else:
#     print('Нет мест')
