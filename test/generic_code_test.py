__author__ = 'atrimble'

from bigio.codec import generic_codec
from test import simple_module_message
from test import simple_class_message
import logging

logger = logging.getLogger(__name__)


def setup():
    logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)


def teardown():
    pass


def make_assertions(message, truth):
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


def test():
    bytes = generic_codec.encode(simple_module_message)
    message = generic_codec.decode(bytes, simple_module_message)
    make_assertions(message, simple_module_message)

    bytes = generic_codec.encode(simple_class_message.SimpleMessage())
    message = generic_codec.decode(bytes, simple_class_message.SimpleMessage)
    make_assertions(message, simple_class_message.SimpleMessage())
