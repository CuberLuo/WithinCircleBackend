import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:' + os.environ.get('DATABASE_PASSWORD') + '@1.15.134.164/within-circle'
