from datetime import datetime

from ..database import db
from ..utils.user_utils import generate_id_by_snowflake


class UserFollows(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    base_user_id = db.Column(db.BigInteger)
    follow_user_id = db.Column(db.BigInteger)
    follow_date = db.Column(db.DateTime())

    def __init__(self, base_user_id, follow_user_id):
        self.id = generate_id_by_snowflake()
        self.base_user_id = base_user_id
        self.follow_user_id = follow_user_id
        self.follow_date = datetime.now()
