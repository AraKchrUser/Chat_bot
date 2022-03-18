import db_session
from entity import *
from datetime import datetime, time, date
import pandas as pd


# Глобальная инициализация базы данных, создаются все таблицы, которые необходимо заполнить тут
db_session.global_init("postgre1")
db_sess = db_session.create_session()

# # Регисртрация заявителя
# person = Applicant()
# person.chat_id = "1"
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
# # Регистрация сотрудника
# employee = Employee()
# employee.department = "Отдел обслуживания"
# employee.post = "Консультант"
# employee.id_mfc = db_sess.query(MFC).filter(MFC.address == "Центральная ул., 37, село Чигири").first().id_mfc
# person.second_name = "Artur"
# person.first_name = "Asatryan"
# person.passport = "1020 2345678"
# person.gender = "M"
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

# # Регистрация на прием
# registr = Registration()
# registr.date_registration = datetime.now()
# registr.date_admission = datetime.combine(date(2022, 7, 14), time(12, 30))
# registr.status = True
# registr.id_service
# registr.id_emp
# registr.id_mfc
# registr.id_app


# print(db_sess.query(MFC).filter(MFC.address == "Центральная ул., 37, село Чигири").first().id_mfc)

# for mfc in db_sess.query(MFC).all():
#     if mfc.address == "Центральная ул., 37, село Чигири":
#         print(mfc.address)
