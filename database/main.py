import db_session
from entity import *


# Глобальная инициализация базы данных, создаются все таблицы, которые необходимо заполнить тут
db_session.global_init("postgres")
db_sess = db_session.create_session()

# user = User()
# user.name = "Пользователь 3"
# user.about = "биография пользователя 3"
# user.email = "email@email3.ru"

# db_sess.add(user)
# db_sess.commit()

# for user in db_sess.query(User).all():
#     print(user.name)
