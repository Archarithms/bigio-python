__author__ = 'atrimble'


from bigio.util import network_util
import socket
from bigio.reactor import Reactor
import bigio.listener_registry as listener_registry
import bigio.codec.gossip_decoder as gossip_decoder
import bigio.parameters as parameters
from bigio.codec.envelope_decoder import EnvelopeDecoder
from bigio.member.member import Member
from bigio.util.configuration import *
import threading
import logging
import socketserver

logger = logging.getLogger(__name__)

gossip_reactor = Reactor()


def send(envelope):
    #if not envelope.decoded:
    #    envelope.message = EnvelopeDecoder.decode(envelope.payload)
    #    envelope.decoded = True

    listener_registry.send(envelope)


class GossipHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global gossip_reactor
        data = self.request.recv(1024)
        data = bytearray(data)[2:]

        if len(data) > 0:
            message = gossip_decoder.decode(data)
            gossip_reactor.emit('gossip', message)


class DataHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)

        if len(data) > 0:
            message = EnvelopeDecoder.decode(data)
            message.decoded = False
            send(message)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    timeout = None
    daemon_threads = True
    pass


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    allow_reuse_address = True
    timeout = None
    daemon_threads = True
    pass


class MeMember(Member):

    def __init__(self):
        protocol = parameters.get_property(PROTOCOL_PROPERTY, DEFAULT_PROTOCOL)
        address = parameters.get_property(ADDRESS_PROPERTY, DEFAULT_ADDRESS)
        gossip_port = parameters.get_property(GOSSIP_PORT_PROPERTY)
        data_port = parameters.get_property(DATA_PORT_PROPERTY)

        if not gossip_port:
            gossip_port = network_util.get_free_port()
        if not data_port:
            data_port = network_util.get_free_port()

        if protocol == 'tcp':

            self.gossip_server = ThreadedTCPServer((address, gossip_port), GossipHandler)
            self.gossip_server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.gossip_server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.gossip_thread = threading.Thread(target=self.gossip_server.serve_forever)

            self.data_server = ThreadedTCPServer((address, data_port), DataHandler)
            self.data_server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.data_server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.data_thread = threading.Thread(target=self.data_server.serve_forever)

            logger.info('Starting TCP node on gossip port ' + str(gossip_port) + ' : data port ' + str(data_port))

        else:
            self.gossip_server = ThreadedUDPServer((address, gossip_port), GossipHandler)
            self.gossip_thread = threading.Thread(target=self.gossip_server.serve_forever)

            self.data_server = ThreadedUDPServer((address, data_port), DataHandler)
            self.data_thread = threading.Thread(target=self.data_server.serve_forever)

            logger.info('Starting UDP node on gossip port ' + str(gossip_port) + ' : data port ' + str(data_port))

        self.gossip_thread.daemon = True
        self.gossip_thread.start()
        self.data_thread.daemon = True
        self.data_thread.start()

        self.ip = address
        self.gossip_port = gossip_port
        self.data_port = data_port

        logger.info('Node started')

        return

    def shutdown(self):
        self.gossip_server.shutdown()
        self.data_server.shutdown()

    @staticmethod
    def add_gossip_consumer(function):
        global gossip_reactor
        gossip_reactor.on('gossip', function)

    def get_protocol(self):
        return self.protocol

    def __str__(self):
        return 'Local member ' + str(self.ip) + ':' + str(self.gossip_port) + ':' + str(self.data_port)