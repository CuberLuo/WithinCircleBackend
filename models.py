from datetime import datetime

from database import db
from utils.timeUtils import getTimeId


class Users(db.Model):
    # 根据当前时间戳自动生成id(微秒级)
    id = db.Column(db.BigInteger, primary_key=True, default=getTimeId())
    username = db.Column(db.String(10))
    password = db.Column(db.String(64))
    registerDate = db.Column(db.DateTime(), default=datetime.now())
