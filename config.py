from datetime import timedelta
import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:pass123@localhost/labct2'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=62)
    SECRET_KEY = 'GnqROcKzl3'
    DEBUG = True