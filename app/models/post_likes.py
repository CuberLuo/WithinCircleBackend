from datetime import datetime

from ..database import db
from ..utils.user_utils import generate_id_by_snowflake


class PostLikes(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    post_id = db.Column(db.BigInteger)
    user_id = db.Column(db.BigInteger)
    like_date = db.Column(db.DateTime())

    def __init__(self, post_id, user_id):
        self.id = generate_id_by_snowflake()
        self.post_id = post_id
        self.user_id = user_id
        self.like_date = datetime.now()
