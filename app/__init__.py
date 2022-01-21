from app import views  # important to retrieve routes despite not being strictly used, must be in last line, otherwise routes will not be retrieved
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_BINDS'] = ""
# app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'app/static/images'
db = SQLAlchemy(app)

app.config.from_object(__name__)
