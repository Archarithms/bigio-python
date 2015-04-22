__author__ = 'atrimble'


class Envelope:
    sender_key = None
    execute_time = 0
    milliseconds_since_midnight = 0
    topic = None
    partition = None
    class_name = None
    payload = None
    key = None
    encrypted = False
    message = None