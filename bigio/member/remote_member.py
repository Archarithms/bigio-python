__author__ = 'atrimble'

from bigio.member.member import Member
from bigio.member.member_status import MemberStatus
from bigio.codec import gossip_encoder
import logging
import socket

logger = logging.getLogger(__name__)


class RemoteMember(Member):

    def __init__(self, use_tcp=True):
        super().__init__()
        self.tcp = use_tcp
        self.gossip_client = None
        self.data_client = None

    def initialize(self):
        if self.tcp:
            try:
                self.gossip_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.gossip_client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                self.gossip_client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                self.gossip_client.connect((self.ip, self.gossip_port))
            except socket.error:
                self.shutdown()

            try:
                self.data_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.data_client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                self.data_client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                self.data_client.connect((self.ip, self.data_port))
            except socket.error:
                self.shutdown()

        else:
            logger.warn('UDP connections not yet implemented.')

        self.status = MemberStatus.Alive

    def shutdown(self):
        logger.info('Shutting down remote member connections ' + str(self))
        self.gossip_client.close()
        self.data_client.close()

    def gossip(self, message):
        try:
            data = gossip_encoder.encode(message)
            self.gossip_client.sendall(data)
        except ConnectionAbortedError:
            pass

    def send(self, message):
        pass

    def __str__(self):
        return self.ip + ':' + str(self.gossip_port) + ':' + str(self.data_port)