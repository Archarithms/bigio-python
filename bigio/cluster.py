
__author__ = 'atrimble'

import logging

from bigio.member.member_holder import MemberHolder
from bigio.mc_discovery import MCDiscovery
from bigio.member.me_member import MeMember
from bigio.member.member_status import MemberStatus
import bigio.listener_registry as listener_registry
from bigio.gossiper import Gossiper
import bigio.parameters as parameters
from bigio.util.configuration import *
from bigio.member.remote_member import RemoteMember
import bigio.util.topic_utils as topic_utils

logger = logging.getLogger(__name__)

me = None


class Cluster:

    mc = None
    gossiper = None
    member_holder = None

    shutting_down = False

    def __init__(self):
        global me

        self.member_holder = MemberHolder()

        me = MeMember()
        me.status = MemberStatus.Alive
        self.member_holder.update_member_status(me)

        me.add_gossip_consumer(self.handle_gossip_message)

        self.mc = MCDiscovery(me)
        self.mc.setup_networking()

        listener_registry.initialize(me)

        self.gossiper = Gossiper(me, self.member_holder)

    def shutdown(self):
        self.shutting_down = True
        global me
        me.shutdown()
        self.mc.shutdown()
        self.gossiper.shutdown()
        for key, member in self.member_holder.get_all_members():
            self.member_holder.get_member(key).shutdown()

    def handle_gossip_message(self, message):
        if self.shutting_down:
            return

        sender_key = str(message.ip) + ':' + str(message.gossip_port) + ':' + str(message.data_port)
        update_tags = False

        logger.info(message)

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

                to_remove = []
                for reg in listener_registry.get_all_registrations():
                    if reg.member == m:
                        # member reporting on itself - take its listener list as cannon
                        if reg.topic not in topics:
                            to_remove.append(reg)

                listener_registry.remove_registrations(to_remove)

                for topic_string in topics:
                    topic = topic_utils.get_topic(topic_string)
                    partition = topic_utils.get_partition(topic_string)
                    if m not in listener_registry.get_registered_members(topic):
                        listener_registry.register_member_for_topic(topic, partition, m)

            if update_tags:
                m = self.member_holder.get_member(sender_key)
                m.tags = message.tags
