from flask import Flask
import telegram as tg
from config import Config

flask_app = Flask(__name__)


from app import main
