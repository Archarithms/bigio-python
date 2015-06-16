__author__ = 'atrimble'


from bigio.util import network_util
import socket
from threading import Timer
from bigio.reactor import Reactor
import bigio.codec.gossip_codec as gossip_decoder
import bigio.parameters as parameters
import bigio.codec.envelope_codec as envelope_codec
from bigio.member.member import Member
from bigio.util.configuration import *
import bigio.util.utils as utils
import threading
import logging
import socketserver

logger = logging.getLogger(__name__)


class GossipHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server, callback):
        self.callback = callback
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        data = self.request.recv(1024)
        data = bytearray(data)[2:]

        if len(data) > 0:
            message = gossip_decoder.decode(data)
            self.callback(message)


class DataHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server, reactor):
        self.reactor = reactor
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        data = self.request.recv(1024)

        if len(data) > 0:
            message = envelope_codec.decode(data)
            self.callback(message)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    timeout = None
    daemon_threads = True

    def __init__(self, server_address, RequestHandlerClass, callback, bind_and_activate=True):
        self.callback = callback
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self, self.callback)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    allow_reuse_address = True
    timeout = None
    daemon_threads = True

    def __init__(self, server_address, RequestHandlerClass, callback, bind_and_activate=True):
        self.callback = callback
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self, self.callback)


class SendTimer(Timer):

    def __init__(self, reactor, timeout, topic, message):
        super().__init__(timeout, self.execute)
        self.reactor = reactor
        self.topic = topic
        self.message = message

    def execute(self):
        self.reactor.emit(self.topic, self.message)


class MeMember(Member):

    def __init__(self):
        super().__init__()
        self.interceptors = dict()
        self.data_reactor = Reactor()
        self.gossip_reactor = Reactor()

        protocol = parameters.get_property(PROTOCOL_PROPERTY, DEFAULT_PROTOCOL)
        address = parameters.get_property(ADDRESS_PROPERTY, DEFAULT_ADDRESS)
        gossip_port = parameters.get_property(GOSSIP_PORT_PROPERTY)
        data_port = parameters.get_property(DATA_PORT_PROPERTY)

        if not gossip_port:
            gossip_port = network_util.get_free_port()
        if not data_port:
            data_port = network_util.get_free_port()

        if protocol == 'tcp':

            self.gossip_server = ThreadedTCPServer((address, gossip_port), GossipHandler, self.gossip)
            self.gossip_server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.gossip_server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.gossip_thread = threading.Thread(target=self.gossip_server.serve_forever)

            self.data_server = ThreadedTCPServer((address, data_port), DataHandler, self.send)
            self.data_server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.data_server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.data_thread = threading.Thread(target=self.data_server.serve_forever)

            logger.info('Starting TCP node on gossip port ' + str(gossip_port) + ' : data port ' + str(data_port))

        else:
            self.gossip_server = ThreadedUDPServer((address, gossip_port), GossipHandler, self.gossip)
            self.gossip_thread = threading.Thread(target=self.gossip_server.serve_forever)

            self.data_server = ThreadedUDPServer((address, data_port), DataHandler, self.send)
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

    def add_gossip_consumer(self, function):
        self.gossip_reactor.on('gossip', function)

    def add_interceptor(self, topic, interceptor):
        if topic not in self.interceptors:
            self.interceptors[topic] = []

        self.interceptors[topic].append(interceptor)

    def send(self, envelope):
        if envelope.topic in self.interceptors:
            for interceptor in self.interceptors[envelope.topic]:
                envelope = interceptor(envelope)

        if envelope.execute_time > 0:
            t = SendTimer(self, self.data_reactor, envelope.execute_time * 1000, envelope.topic, envelope.message)
            t.start()
        elif envelope.execute_time >= 0:
            self.data_reactor.reactor.emit(envelope.topic, envelope.message)

    def gossip(self, envelope):
        self.gossip_reactor.emit('gossip', envelope)

    def add_local_listener(self, topic, listener):
        self.data_reactor.on(topic, listener)

    def __str__(self):
        return 'Local member ' + utils.get_key(self)