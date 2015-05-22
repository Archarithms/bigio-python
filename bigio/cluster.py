
__author__ = 'atrimble'

import logging

import bigio.codec.generic_codec as generic_encoder
from bigio.member.member_holder import MemberHolder
from bigio.mc_discovery import MCDiscovery
from bigio.member.me_member import MeMember
from bigio.member.member_status import MemberStatus
from bigio.listener_registry import ListenerRegistry
from bigio.gossiper import Gossiper
from bigio.envelope import Envelope
import bigio.parameters as parameters
from bigio.util.configuration import *
from bigio.util import utils
from bigio.util import time_util as time_util
from bigio.member.remote_member import RemoteMember
import bigio.util.topic_utils as topic_utils

logger = logging.getLogger(__name__)


class Cluster:

    def __init__(self):

        self.shutting_down = False

        self.member_holder = MemberHolder()

        self.me = MeMember()
        self.me.status = MemberStatus.Alive
        self.member_holder.update_member_status(self.me)

        self.me.add_gossip_consumer(self.handle_gossip_message)

        self.mc = MCDiscovery(self.me)
        self.mc.setup_networking()

        self.listener_registry = ListenerRegistry(self.me, self.member_holder)

        self.gossiper = Gossiper(self.me, self.member_holder, self.listener_registry)

    def shutdown(self):
        self.shutting_down = True
        self.me.shutdown()
        self.mc.shutdown()
        self.gossiper.shutdown()
        for member in self.member_holder.get_all_members():
            member.shutdown()

    def add_listener(self, topic, listener, partition=None):
        self.listener_registry.register_member_for_topic(topic, self.me)
        self.listener_registry.add_local_listener(topic, listener)

    def add_interceptor(self, topic, interceptor):
        self.listener_registry.add_interceptor(topic, interceptor)

    def send(self, message, topic, partition=None, offset=None, java_class=None):
        envelope = Envelope()
        envelope.decoded = False
        if offset is not None:
            envelope.execute_time = offset
        else:
            envelope.execute_time = 0
        envelope.milliseconds_since_midnight = time_util.get_milliseconds_since_midnight()
        envelope.sender_key = utils.get_key(self.me)
        envelope.topic = topic
        if partition is not None:
            envelope.partition = partition
        else:
            envelope.partition = ''
        if java_class is not None:
            envelope.class_name = java_class
        else:
            envelope.class_name = ''

        members = self.listener_registry.get_registered_members(topic)
        for member in members:
            if self.me == member:
                envelope.payload = message
                envelope.decoded = True
            else:
                envelope.payload = generic_encoder.encode(message)
                envelope.decoded = False

            member.send(envelope)

    def handle_gossip_message(self, message):
        if self.shutting_down:
            return

        sender_key = utils.get_key(ip=message.ip, gossip_port=message.gossip_port, data_port=message.data_port)
        update_tags = False

        for i in range(0, len(message.members)):
            key = message.members[i]
            m = self.member_holder.get_member(key)

            if m is None:
                protocol = parameters.get_property(PROTOCOL_PROPERTY, DEFAULT_PROTOCOL)
                if protocol == 'udp':
                    logger.debug("Discovered new UDP member through gossip: " + str(message.getIp()) + ":" + str(message.getGossipPort()) + ":" + str(message.getDataPort()))
                    m = RemoteMember(use_tcp=False)
                else:
                    logger.debug("Discovered new TCP member through gossip: " + str(message.ip) + ":" + str(message.gossip_port) + ":" + str(message.data_port))
                    m = RemoteMember(use_tcp=True)

                values = key.split(":")
                m.ip = values[0]
                m.gossip_port = int(values[1])
                m.data_port = int(values[2])
                if message.public_key:
                    m.public_key = message.public_key

                m.initialize()

            self.member_holder.update_member_status(m)

            member_clock = message.clock[i]
            known_member_clock = m.sequence

            if member_clock > known_member_clock:
                if key == sender_key:
                    update_tags = True

                m.sequence = member_clock
                if key in message.listeners:
                    topics = message.listeners[key]
                else:
                    topics = []

                for topic, member_list in self.listener_registry.get_all_registrations().items():
                    if key in member_list:
                        # member reporting on itself - take its listener list as canon
                        if topic not in topics:
                            self.listener_registry.remove_registration(m, topic)

                for topic_string in topics:
                    topic = topic_utils.get_topic(topic_string)
                    partition = topic_utils.get_partition(topic_string)
                    if m not in self.listener_registry.get_registered_members(topic):
                        self.listener_registry.register_member_for_topic(topic, partition, m)

            if update_tags:
                m = self.member_holder.get_member(sender_key)
                m.tags = message.tags
