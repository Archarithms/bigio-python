__author__ = 'atrimble'

from datetime import datetime


def get_milliseconds_since_midnight():
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (now - midnight).seconds
    return int(seconds * 1000)
