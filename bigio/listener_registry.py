__author__ = 'atrimble'

from threading import Timer
from bigio.reactor import Reactor
from bigio.member.registration import Registration


class ListenerRegistry:

    def __init__(self, member):
        self.reactor = Reactor()
        self.interceptors = dict()
        self.me = member
        self.map = dict()

    def add_interceptor(self, topic, interceptor):
        if topic not in self.interceptors:
            self.interceptors[topic] = []

        self.interceptors[topic].append(interceptor)

    def add_local_listener(self, topic, partition, listener):
        self.reactor.on(topic, listener)

    def register_member_for_topic(self, topic, member):
        key = member.ip + ':' + member.gossip_port + ':' + member.data_port

        if key not in self.map:
            self.map[key] = {}

        if topic not in self.map[key]:
            self.map[key][topic] = []

        found = False
        for reg in self.map[key][topic]:
            if topic == reg.topic and member == reg.member:
                found = True
                break

        if not found:
            reg = Registration()
            reg.member = member
            reg.topic = topic
            self.map[key][topic].append(reg)

    def get_all_registrations(self):
        ret = []
        for key in self.map:
            for topic in self.map[key]:
                for reg in self.map[key][topic]:
                    ret.append(reg)
        return ret


    def get_registered_members(self, topic):
        ret = []

        for key in self.map:
            if topic in self.map[key]:
                for reg in self.map[key][topic]:
                    ret.append(reg.member)

        return ret

    def remove_registrations(self, regs):
        for key in self.map:
            for reg in self.map[key]:
                if reg in regs:
                    self.map[key].pop(reg)

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