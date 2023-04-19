from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dateutil import parser

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


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = parser.parse(date)
    native = date.replace(tzinfo=None)
    date_format = '%d/%m/%Y'
    return native.strftime(date_format)


from app import routes


# open shell and run python command:
#   from app import app, db
