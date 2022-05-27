import flask
from flask import jsonify, request, render_template, url_for
from passport_process import mrz_opencv
from database.entity import *
from database.db_session import *
from transliterate import translit


blueprint = flask.Blueprint('route_api', __name__, template_folder='template')


@blueprint.route('/api/news/<float:point11>/<float:point12>/<string:point2>', methods=['GET', 'POST'])
def get_route(point11, point12, point2):
    # 'ул. 50 лет Октября, 61, Благовещенск, Россия'
    # 'ул. Мухина, 114, Благовещенск, Россия'
    # return jsonify({"/api": "/news"})
    if request.method == "GET":
        return render_template('2api.html', point1=[point11, point12], point2=point2)
    print(request)


@blueprint.route('/api/passport/', methods=['GET', 'POST'])
def get_coord():
    if request.method == 'GET':
        return render_template('index.html', style_path=url_for('static', filename='css/style.css'),
                           text='', question='', answer='',
                           user_name='')
    if request.method == 'POST':
        if request.form["accept"]:

            global_init("postgre1")

            db_session = create_session()
            usr = db_session.query(Applicant).filter(Applicant.chat_id == str(request.form['chat-id'])).first()
            if usr:
                regs = db_session.query(Registration).filter(Registration.id_app == usr.id_app).all()
                for reg in regs:
                    db_session.delete(reg)
                    db_session.commit()
                db_session.delete(usr)
                db_session.commit()

            private_data = mrz_opencv(bytes=request.files['file'].read()).replace("<", " ").split()
            print(private_data)
            first_name, second_name = private_data[2].lower().split('k')[:-1]
            first_name, second_name = translit(first_name.title(), "ru"), translit(second_name.title(), "ru")
            passport = private_data[4][:-1]
            gender = 'муж' if private_data[4][-1] == 'F' else 'жен'
            print(first_name, second_name, passport, gender)

            db_sess = create_session()
            person = Applicant()
            person.chat_id = request.form['chat-id']
            person.verified = True
            person.second_name = second_name
            person.first_name = first_name
            person.passport = passport
            person.gender = gender
            db_sess.add(person)
            db_sess.commit()

        return render_template('index.html', style_path=url_for('static', filename='css/style.css'),
                           text='', question='', answer='',
                           user_name='')
