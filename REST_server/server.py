import route_api
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.register_blueprint(route_api.blueprint)
    app.run(host='0.0.0.0', port=4567)


main()
