from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from jinja2 import Environment

plant_app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

plant_app.config.update(
    SECRET_KEY='this-is-a-secret',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),   #sets location of database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)
db = SQLAlchemy(plant_app)
migrate = Migrate(plant_app,db)

login = LoginManager(plant_app)

login.login_view = 'login'
login.refresh_view = 'relogin'
login.needs_refresh_message = ('Session timed out, please re-login')
login.needs_refresh_message_category = 'info'

from app import routes, models