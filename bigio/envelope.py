__author__ = 'atrimble'


class Envelope:
    def __init__(self):
        self.sender_key = None
        self.execute_time = 0
        self.milliseconds_since_midnight = 0
        self.topic = None
        self.partition = None
        self.class_name = None
        self.payload = None
        self.key = None
        self.encrypted = False
        self.message = None