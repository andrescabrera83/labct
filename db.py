import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', Config.SECRET_KEY)
app.config.from_object(Config)
  # Set session expiration to 62 days
db = SQLAlchemy(app)
ma = Marshmallow(app)
