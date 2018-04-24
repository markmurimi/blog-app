import os

class Config:
    """main configuration class"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://mark:mark123@localhost/blog'

    SECRET_KEY = "victor01"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://mark:victor01@localhost/blog'


class DevConfig(Config):
    DEBUG = True

config_options ={
    'development': DevConfig,
    'production': ProdConfig
}
