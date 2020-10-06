import os

class Config(object):
    SECRET_KEY= os.environ.get('SECRET_KEY')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MY_MAIL')
    MAIL_PASSWORD = os.environ.get('MY_PASS')

class DevelopmentConfig(Config):
    DEBUG = True#False
    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')
    host = os.environ.get('POSTGRES_HOST')
    database = os.environ.get('POSTGRES_DB')
    port = os.environ.get('POSTGRES_PORT')
    #DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    print(f'{SQLALCHEMY_DATABASE_URI} <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
