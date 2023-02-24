from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/static/uploads/'

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# db.init_app(app)
migrate.init_app(app)

from app import routes



# open shell and run python command:
#   from app import app, db
