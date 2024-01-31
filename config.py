import os
from datetime import timedelta

DOMAIN_NAME = 'techvip.site'
SUB_DOMAIN = 'within-circle'
WEB_BASE_URL = f'https://{SUB_DOMAIN}.{DOMAIN_NAME}'
API_BASE_URL = f'https://api.{SUB_DOMAIN}.{DOMAIN_NAME}'


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:' + os.environ.get('DATABASE_PASSWORD') + '@127.0.0.1/within-circle'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 120,
        'connect_args': {'connect_timeout': 20}
    }
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)  # token有效时长
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=15)  # refreshToken有效时长
