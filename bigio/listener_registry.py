__author__ = 'atrimble'

import logging
from threading import Timer
from bigio.reactor import Reactor
import bigio.util.utils as utils

logger = logging.getLogger(__name__)


class ListenerRegistry:

    def __init__(self, member, member_holder):
        self.reactor = Reactor()
        self.interceptors = dict()
        self.me = member
        self.member_holder = member_holder
        self.map = dict()

    def add_interceptor(self, topic, interceptor):
        if topic not in self.interceptors:
            self.interceptors[topic] = []

        self.interceptors[topic].append(interceptor)

    def add_local_listener(self, topic, listener):
        self.reactor.on(topic, listener)

    def register_member_for_topic(self, topic, member):
        key = utils.get_key(member)

        if key not in self.map:
            self.map[key] = []

        if topic not in self.map[key]:
            self.map[key].append(topic)

    def get_all_registrations(self):
        return self.map

    def get_registered_members(self, topic):
        ret = []

        for key in self.map:
            if topic in self.map[key]:
                ret.append(self.member_holder.get_member(key))

        return ret

    def remove_registration(self, member, topic):
        key = utils.get_key(member)
        if topic in self.map[key]:
            self.map[key].remove(topic)

    def send(self, envelope):
        if envelope.topic in self.interceptors:
            for interceptor in self.interceptors[envelope.topic]:
                envelope = interceptor(envelope)

        if envelope.execute_time > 0:
            t = SendTimer(self, envelope.execute_time * 1000, envelope.topic, envelope.message)
            t.start()
        elif envelope.execute_time >= 0:
            reactor.emit(envelope.topic, envelope.message)

    def send_now(self, topic, message):
        self.reactor.emit(topic, message)


class SendTimer(Timer):

    topic = None
    message = None
    global reactor

    def __init__(self, registry, timeout, topic, message):
        super().__init__(timeout, self.execute)
        self.registry = registry
        self.topic = topic
        self.message = message

    def execute(self):
        self.registry.reactor.emit(self.topic, self.message)