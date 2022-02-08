from app import flask_app, Config
from app.main import init_bot

if __name__ == '__main__':
    flask_app.run(host='localhost')
