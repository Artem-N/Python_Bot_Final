from app import flask_app, Config
from app.views import init_bot


if __name__ == '__main__':
    flask_app.run(debug=True, host='localhost')
