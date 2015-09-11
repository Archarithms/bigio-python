__author__ = 'atrimble'

from bigio.codec import envelope_codec
from test import simple_class_message
from test import simple_module_message
from bigio.envelope import Envelope
from bigio.util import time_util
from bigio.util import utils
import logging

logger = logging.getLogger(__name__)
envelope = Envelope()

def setup():
    logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

    envelope.sender_key = utils.get_key(ip='127.0.0.1', gossip_port=8888, data_port=9999)
    envelope.execute_time = 1
    envelope.milliseconds_since_midnight = time_util.get_milliseconds_since_midnight()
    envelope.topic = 'TestTopic'
    envelope.partition = 'TestPartition'
    envelope.key = None
    envelope.encrypted = False


def teardown():
    pass


def make_envelope_assertions(envelope, truth):
    assert envelope.sender_key == truth.sender_key
    assert envelope.execute_time == truth.execute_time
    assert envelope.milliseconds_since_midnight == truth.milliseconds_since_midnight
    assert envelope.topic == truth.topic
    assert envelope.partition == truth.partition
    assert envelope.type == truth.type
    assert envelope.key == truth.key
    assert envelope.encrypted == truth.encrypted


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


def test_class():
    envelope.message = simple_class_message.SimpleMessage()
    envelope.type = 'test.simple_class_message.SimpleMessage'

    bytes = envelope_codec.encode(envelope)
    message = envelope_codec.decode(bytes[2:])

    make_envelope_assertions(message, envelope)
    make_message_assertions(message.message, envelope.message)


def test_module():
    envelope.message = simple_module_message
    envelope.type = 'test.simple_module_message'

    bytes = envelope_codec.encode(envelope)
    message = envelope_codec.decode(bytes[2:])

    make_envelope_assertions(message, envelope)
    make_message_assertions(message.message, envelope.message)
