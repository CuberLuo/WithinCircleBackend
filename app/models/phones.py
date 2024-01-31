from ..database import db
from ..utils.time_utils import get_time_id


class Phones(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger)
    phone = db.Column(db.String(11))
    code = db.Column(db.String(5))
    expire_time = db.Column(db.DateTime())

    def __init__(self, phone):
        self.id = get_time_id()
        self.phone = phone
