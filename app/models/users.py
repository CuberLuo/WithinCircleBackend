from datetime import datetime

from config import WEB_BASE_URL
from ..database import db
from ..utils.time_utils import get_time_id


class Users(db.Model):
    # 根据当前时间戳自动生成id(微秒级)
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(10))
    password = db.Column(db.String(64))
    gender = db.Column(db.String(10), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(100), nullable=True)
    avatar_url = db.Column(db.String(1024), nullable=True)
    register_date = db.Column(db.DateTime())

    def __init__(self, username, password):
        self.id = get_time_id()
        self.username = username
        self.password = password
        self.avatar_url = f'{WEB_BASE_URL}/images/default_user.jpg'
        self.register_date = datetime.now()
