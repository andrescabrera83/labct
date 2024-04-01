import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config
from flask_migrate import Migrate


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', Config.SECRET_KEY)
app.config.from_object(Config)
  # Set session expiration to 62 days
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
