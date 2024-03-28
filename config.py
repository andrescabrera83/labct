from datetime import timedelta


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=62)
    SECRET_KEY = 'SOXOZvMJBD'
    DEBUG = False