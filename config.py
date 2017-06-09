import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    SECRET_KEY = 'my_carto_app'
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/afr_cartix'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
