__author__ = 'atrimble'

from bigio.reactor import Reactor
import logging
import threading

main_thread = -1
thread_ident_1 = -1
thread_ident_2 = -1

received = False
received2 = False
message = 'this is a test message'

logger = logging.getLogger(__name__)


def setup():
    logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)


def teardown():
    pass


def receive(msg):
    global received
    global message
    global thread_ident_1
    received = True
    assert msg == message
    thread_ident_1 = threading.current_thread().ident


def receive_mult(msg):
    global received2
    global thread_ident_2
    received2 = True
    thread_ident_2 = threading.current_thread().ident


def test():
    global main_thread
    global thread_ident_1
    global thread_ident_2
    global received
    global message

    main_thread = threading.current_thread().ident

    reactor = Reactor()
    reactor.on('test', receive)
    reactor.emit('test', message)
    assert received

    received = False
    reactor.emit('test1', message)
    assert not received

    reactor.on('mult', receive)
    reactor.on('mult', receive_mult)
    reactor.emit('mult', message)
    assert received and received2

    assert main_thread != thread_ident_1 and main_thread != thread_ident_2 and thread_ident_1 != thread_ident_2
