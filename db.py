import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config
from flask_migrate import Migrate
from sqlalchemy import MetaData

metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }
)


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', Config.SECRET_KEY)
app.config.from_object(Config)
  # Set session expiration to 62 days
db = SQLAlchemy(app, metadata=metadata)
ma = Marshmallow(app)
migrate = Migrate(app, db)
