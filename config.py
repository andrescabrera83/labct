from datetime import timedelta
import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:mY_password4321@localhost/labct'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=62)
    SECRET_KEY = 'GnqROcKzl3'
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = False
