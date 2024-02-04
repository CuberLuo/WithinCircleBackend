from datetime import datetime

from ..database import db
from ..utils.user_utils import generate_id_by_snowflake


class Posts(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger)
    post_msg = db.Column(db.String(510))
    visible_circle = db.Column(db.Integer)
    post_date = db.Column(db.DateTime())
    loc_name = db.Column(db.String(255))
    lat = db.Column(db.String(255))
    lon = db.Column(db.String(255))
    like_num = db.Column(db.Integer)

    def __init__(self, user_id, post_msg, visible_circle, loc_name, lat, lon):
        self.id = generate_id_by_snowflake()
        self.post_date = datetime.now()
        self.user_id = user_id
        self.post_msg = post_msg
        self.visible_circle = visible_circle
        self.loc_name = loc_name
        self.lat = lat
        self.lon = lon
        self.like_num = 0
