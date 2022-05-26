import flask
from flask import jsonify, request, render_template, url_for
from passport_process import mrz_opencv

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
        print(mrz_opencv(bytes=request.files['file'].read()))
        return jsonify({"ok": "200"})
