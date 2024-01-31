from datetime import datetime

from ..database import db
from ..utils.time_utils import get_time_id


class PostLikes(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    post_id = db.Column(db.BigInteger)
    user_id = db.Column(db.BigInteger)
    like_date = db.Column(db.DateTime())

    def __init__(self, post_id, user_id):
        self.id = get_time_id()
        self.post_id = post_id
        self.user_id = user_id
        self.like_date = datetime.now()
