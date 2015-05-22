__author__ = 'atrimble'


import socket
import struct
import threading
import logging
import bigio.parameters as parameters
from bigio.util.configuration import *
from bigio.gossip_message import GossipMessage
import bigio.util.time_util as time_util
import bigio.codec.gossip_codec as gossip_codec

logger = logging.getLogger(__name__)


class MCDiscovery:

    def __init__(self, me):
        self.should_shutdown = False
        self.sock = None
        self.group = parameters.get_property(MULTICAST_GROUP_PROPERTY, DEFAULT_MULTICAST_GROUP)
        self.port = int(parameters.get_property(MULTICAST_PORT_PROPERTY, DEFAULT_MULTICAST_PORT))
        self.address = parameters.get_property(ADDRESS_PROPERTY, DEFAULT_ADDRESS)
        self.me = me
        self.listen_thread = None

    def setup_networking(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.port))
        self.sock.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            struct.pack('4sL',
                        socket.inet_aton(self.group),
                        socket.INADDR_ANY))

        self.listen_thread = threading.Thread(target=self.listen)
        self.listen_thread.daemon = True
        self.listen_thread.start()

        self.announce()

    def shutdown(self):
        self.should_shutdown = True

    def listen(self):
        while not self.should_shutdown:
            data, address = self.sock.recvfrom(65507)
            data = data[2:]
            message = gossip_codec.decode(data)
            self.me.gossip_reactor.emit('gossip', message)

        self.sock.close()

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

        data = gossip_codec.encode(message)

        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ttl = struct.pack('b', 1)
        server .setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.sendto(data, (self.group, self.port))
        server.close()
