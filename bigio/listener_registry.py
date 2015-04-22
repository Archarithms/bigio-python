__author__ = 'atrimble'

from threading import Timer
from bigio.reactor import Reactor
from bigio.member.registration import Registration


reactor = Reactor()
interceptors = dict()
me = None
map = dict()


def initialize(member):
    global me
    me = member


def add_interceptor(topic, interceptor):
    if topic not in interceptors:
        interceptors[topic] = []

    interceptors[topic].append(interceptor)


def add_local_listener(topic, partition, listener):
    reactor.on(topic, listener)


def register_member_for_topic(topic, member):
    key = member.ip + ':' + member.gossip_port + ':' + member.data_port

    if key not in map:
        map[key] = {}

    if topic not in map[key]:
        map[key][topic] = []

    found = False
    for reg in map[key][topic]:
        if topic == reg.topic and member == reg.member:
            found = True
            break

    if not found:
        reg = Registration()
        reg.member = member
        reg.topic = topic
        map[key][topic].append(reg)


def get_all_registrations():
    ret = []
    for key in map:
        for topic in map[key]:
            for reg in map[key][topic]:
                ret.append(reg)
    return ret


def get_registered_members(topic):
    ret = []

    for key in map:
        if topic in map[key]:
            for reg in map[key][topic]:
                ret.append(reg.member)

    return ret


def remove_registrations(regs):
    for key in map:
        for reg in map[key]:
            if reg in regs:
                map[key].pop(reg)


def send(envelope):
    if envelope.topic in interceptors:
        for interceptor in interceptors[envelope.topic]:
            envelope = interceptor(envelope)

    if envelope.execute_time > 0:
        t = SendTimer(envelope.execute_time * 1000, envelope.topic, envelope.message)
        t.start()
    elif envelope.execute_time >= 0:
        reactor.emit(envelope.topic, envelope.message)


def send_now(topic, message):
    reactor.emit(topic, message)


class SendTimer(Timer):

    topic = None
    message = None
    global reactor

    def __init__(self, timeout, topic, message):
        super().__init__(timeout, self.execute)
        self.topic = topic
        self.message = message

    def execute(self):
        reactor.emit(self.topic, self.message)