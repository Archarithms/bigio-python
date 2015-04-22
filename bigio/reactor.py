__author__ = 'atrimble'


from threading import Thread
import logging

logger = logging.getLogger(__name__)


class NotifierThread(Thread):

    message = None

    def __init__(self, handler, message):
        super().__init__()
        self.handler = handler
        self.message = message

    def run(self):
        self.handler(self.message)


class Reactor(object):

    def __init__(self, name=None):
        self.name = name
        self.handlers = {}

    def on(self, event_name, handler):
        """Binds an event to a function."""
        handlers = self.handlers.get(event_name, [])
        if handler not in handlers:
            handlers.append(handler)
            self.handlers[event_name] = handlers

    def off(self, event_name, handler):
        """Unbinds an event to a function."""
        handlers = self.handlers.get(event_name, [])
        handlers.remove(handler)

    def emit(self, event_name, message):
        """Calls an event. You can also pass arguments."""
        handlers = self.handlers.get(event_name, [])
        for handler in handlers:
            NotifierThread(handler, message=message).start()

