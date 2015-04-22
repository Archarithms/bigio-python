__author__ = 'atrimble'


import socket
import threading
import logging
import bigio.parameters as parameters
from bigio.util.configuration import *
from bigio.gossip_message import GossipMessage
import bigio.util.time_util as time_util
import bigio.codec.gossip_encoder as gossip_encoder
import bigio.codec.gossip_decoder as gossip_decoder
from bigio.member import me_member

logger = logging.getLogger(__name__)


class MCDiscovery:

    should_shutdown = False
    client = None
    address = None
    me = None

    group = ''
    port = 0

    listen_thread = None

    def __init__(self, me):
        self.group = parameters.get_property(MULTICAST_GROUP_PROPERTY, DEFAULT_MULTICAST_GROUP)
        self.port = int(parameters.get_property(MULTICAST_PORT_PROPERTY, DEFAULT_MULTICAST_PORT))
        self.address = parameters.get_property(ADDRESS_PROPERTY, DEFAULT_ADDRESS)
        self.me = me

    def setup_networking(self):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        self.client.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        self.client.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(socket.gethostbyname(self.address)))
        self.client.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(self.group) + socket.inet_aton(socket.gethostbyname(self.address)))
        self.client.bind((self.address, self.port))

        listen_thread = threading.Thread(target=self.listen)
        listen_thread.daemon = True
        listen_thread.start()

        self.announce()

    def shutdown(self):
        self.should_shutdown = True

    def listen(self):
        while not self.should_shutdown:
            data = self.client.recv(65507)
            data = bytearray(data)[2:]
            message = gossip_decoder.decode(data)
            me_member.gossip_reactor.emit('gossip', message)

        self.client.close()

    def announce(self):
        logger.info("Announcing")
        message = GossipMessage()
        message.ip = self.me.ip
        message.gossip_port = self.me.gossip_port
        message.data_port = self.me.data_port
        message.milliseconds_since_midnight = time_util.get_milliseconds_since_midnight()
        for key in self.me.tags:
            message.tags[key] = self.me.tags[key]

        message.members = [self.me.ip + ":" + str(self.me.gossip_port) + ":" + str(self.me.data_port)]
        self.me.sequence += 1
        message.clock.append(self.me.sequence)
        message.public_key = self.me.public_key

        data = gossip_encoder.encode(message)
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        server.sendto(data, (self.group, self.port))
        server.close()
