from datetime import datetime

from ..database import db
from ..utils.timeUtils import getTimeId


class Users(db.Model):
    # 根据当前时间戳自动生成id(微秒级)
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(10))
    password = db.Column(db.String(64))
    gender = db.Column(db.String(10), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(100), nullable=True)
    avatarUrl = db.Column(db.String(1024), nullable=True)
    registerDate = db.Column(db.DateTime())

    def __init__(self, username, password):
        self.id = getTimeId()
        self.username = username
        self.password = password
        self.registerDate = datetime.now()
