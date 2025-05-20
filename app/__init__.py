import os

from flask import Flask
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'app/static/uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['UPLOAD_FOLDER'] + "images"):
    os.makedirs(app.config['UPLOAD_FOLDER']  + "images")

if not os.path.exists(app.config['UPLOAD_FOLDER']  + "voices"):
    os.makedirs(app.config['UPLOAD_FOLDER'] + "voices")
    

from app import routes
