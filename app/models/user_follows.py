from datetime import datetime

from ..database import db
from ..utils.time_utils import get_time_id


class UserFollows(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    base_user_id = db.Column(db.BigInteger)
    follow_user_id = db.Column(db.BigInteger)
    follow_date = db.Column(db.DateTime())

    def __init__(self, base_user_id, follow_user_id):
        self.id = get_time_id()
        self.base_user_id = base_user_id
        self.follow_user_id = follow_user_id
        self.follow_date = datetime.now()
