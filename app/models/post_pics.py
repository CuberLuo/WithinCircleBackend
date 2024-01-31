from ..database import db
from ..utils.time_utils import get_time_id


class PostPics(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    post_id = db.Column(db.BigInteger)
    pic_link = db.Column(db.String(255))

    def __init__(self, post_id, pic_link):
        self.id = get_time_id()
        self.post_id = post_id
        self.pic_link = pic_link
