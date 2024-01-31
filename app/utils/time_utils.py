import time
from datetime import datetime


def get_time_id():
    t = time.time()
    time_id = int(t * 1000000)
    return time_id


def get_current_date_time():
    return datetime.now()
