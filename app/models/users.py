from datetime import datetime

from config import WEB_BASE_URL
from ..database import db

from ..utils.user_utils import generate_id_by_snowflake


class Users(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(10))
    password = db.Column(db.String(64))
    gender = db.Column(db.String(10), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    avatar_url = db.Column(db.String(1024), nullable=True)
    register_date = db.Column(db.DateTime())

    def __init__(self, username, password):
        self.id = generate_id_by_snowflake()
        self.username = username
        self.password = password
        self.avatar_url = f'{WEB_BASE_URL}/images/default_user.jpg'
        self.register_date = datetime.now()
