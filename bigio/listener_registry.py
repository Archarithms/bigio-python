__author__ = 'atrimble'

import logging

from bigio.reactor import Reactor
import bigio.util.utils as utils

logger = logging.getLogger(__name__)


class ListenerRegistry:

    def __init__(self, me, member_holder):
        self.me = me
        self.member_holder = member_holder
        self.map = dict()

    def add_interceptor(self, topic, interceptor):
        self.me.add_interceptor(topic, interceptor)

    def add_local_listener(self, topic, listener):
        self.me.add_local_listener(topic, listener)

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


