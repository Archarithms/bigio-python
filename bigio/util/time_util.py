__author__ = 'atrimble'

from datetime import datetime


def get_milliseconds_since_midnight():
    now = datetime.now()
    ret = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds
    return 0