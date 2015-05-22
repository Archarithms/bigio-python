__author__ = 'atrimble'


import bigio.parameters as parameters
import random
from threading import Timer
from bigio.util.configuration import *
from bigio.util import utils
from bigio.gossip_message import GossipMessage
import bigio.util.time_util as time_util
import logging

logger = logging.getLogger(__name__)

gossip_interval = parameters.get_property(GOSSIP_INTERVAL_PROPERTY, DEFAULT_GOSSIP_INTERVAL)
cleanup_interval = parameters.get_property(CLEANUP_INTERVAL_PROPERTY, DEFAULT_CLEANUP_INTERVAL)

should_shutdown = False


class Gossiper:

    def __init__(self, me, member_holder, listener_registry):
        self.me = me
        self.member_holder = member_holder
        self.listener_registry = listener_registry
        if not should_shutdown:
            t = GossipThread(self.send_membership)
            t.start()

    def shutdown(self):
        global should_shutdown
        should_shutdown = True

    def send_membership(self):
        member = self.get_random_member()

        if member is not None and member is not self.me:
            message = GossipMessage()
            message.ip = self.me.ip
            message.gossip_port = self.me.gossip_port
            message.data_port = self.me.data_port
            message.milliseconds_since_midnight = time_util.get_milliseconds_since_midnight()
            message.public_key = self.me.public_key
            message.tags = self.me.tags

            for m in self.member_holder.get_active_members():
                message.members.append(utils.get_key(m))
                if m == self.me:
                    self.me.sequence = self.me.sequence + 1
                message.clock.append(m.sequence)

            for r in self.listener_registry.get_all_registrations():
                key = utils.get_key(ip=r.member.ip, gossip_port=r.member.gossip_port, data_port=r.member.data_port)
                if key not in message.listeners:
                    message.listeners[key] = []
                message.listeners[key].append(r.topic)

            member.gossip(message)

        return

    def get_random_member(self):
        members = self.member_holder.get_active_members()
        if len(members) > 1:
            tries = 10
            chosen_member = members[random.randint(0, len(members) - 1)]
            while chosen_member is self.me:
                tries = tries - 1

                if tries < 0:
                    chosen_member = None
                    break

                chosen_member = members[random.randint(0, len(members) - 1)]

            if chosen_member is self.me:
                return None
            else:
                return chosen_member


class GossipThread(Timer):
    func = None

    def __init__(self, func):
        super().__init__(float(gossip_interval) * 1000.0, func)
        self.func = func

    def run(self):
        self.func()
        if not should_shutdown:
            t = GossipThread(self.func)
            t.start()


