import time


def getTimeId():
    t = time.time()
    timeId = int(t * 1000000)
    return timeId
