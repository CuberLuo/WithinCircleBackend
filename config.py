import os
from datetime import timedelta


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:' + os.environ.get('DATABASE_PASSWORD') + '@1.15.134.164/within-circle'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 120,
        'connect_args': {'connect_timeout': 20}
    }
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)
