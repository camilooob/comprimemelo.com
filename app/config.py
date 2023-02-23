import os

class Config:
    """ Clase de configuración de flask. """
    SECRET_KEY = 'eventos secreatas de youtube'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../eventos.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY= 'UatnOQmYhlfQNaINx5OX'
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'franklin.pinto@gmail.com'
    MAIL_PASSWORD = 'jzlgabmqeyxvwyas'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False