import os
from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
secret_key = os.environ.get('FLASK_SECRET_KEY')
app.secret_key = secret_key
app.config.from_object('config.Config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:pass123@localhost/labct2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=62)  # Set session expiration to 62 days
db = SQLAlchemy(app)
ma = Marshmallow(app)
