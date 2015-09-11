__author__ = 'atrimble'

from bigio.bigio import BigIO
from test import simple_class_message
import logging
import sched
import time
import threading

logger = logging.getLogger(__name__)
message = simple_class_message.SimpleMessage()
lock = threading.Semaphore()
received = None
bigio = None


def setup():
    global bigio
    logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    bigio = BigIO()


def teardown():
    global bigio
    bigio.shutdown()
    pass


def make_message_assertions(message, truth):
    assert message.int_num == truth.int_num
    assert message.float_num == truth.float_num
    assert message.string == truth.string
    unmatched = set(message.dictionary.items()) ^ set(truth.dictionary.items())
    assert len(unmatched) == 0
    unmatched = set(message.str_arr) ^ set(truth.str_arr)
    assert len(unmatched) == 0
    unmatched = set(message.int_arr) ^ set(truth.int_arr)
    assert len(unmatched) == 0
    unmatched = set(message.float_arr) ^ set(truth.float_arr)
    assert len(unmatched) == 0


def test_send_receive():
    global received, message, bigio, lock
    lock.acquire()
    bigio.add_listener('HelloWorldLocal', receive)
    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, send, ())
    s.run()
    if lock.acquire(timeout=2):
        make_message_assertions(received, message)
        lock.release()
    else:
        assert False


def receive(recvd):
    global received, lock
    received = recvd
    lock.release()


def send():
    global message, bigio
    bigio.send(message, 'HelloWorldLocal')
