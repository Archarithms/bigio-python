__author__ = 'atrimble'

import logging
from bigio.gossip_message import GossipMessage
from bigio.codec import gossip_codec


logger = logging.getLogger(__name__)


def setup():
    logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)


def teardown():
    pass


def test():
    message = GossipMessage()
    message.ip = '127.0.0.1'
    message.gossip_port = 9999
    message.data_port = 9998
    message.milliseconds_since_midnight = 0
    message.tags = {'tag1': 'value1', 'tag2': 'value2'}
    message.members.append('127.0.0.1:9999:9998')
    message.clock.append(0)
    message.listeners['me'] = []
    message.listeners['me'].append('topic1')

    bytes = gossip_codec.encode(message)
    # Be sure and strip off the two byte length field
    value = gossip_codec.decode(bytes[2:])

    assert value.ip == message.ip
    assert value.gossip_port == message.gossip_port
    assert value.data_port == message.data_port
    assert value.milliseconds_since_midnight == message.milliseconds_since_midnight
    unmatched = set(value.tags.items()) ^ set(message.tags.items())
    assert len(unmatched) == 0
    unmatched = set(value.members) ^ set(message.members)
    assert len(unmatched) == 0
    unmatched = set(value.clock) ^ set(message.clock)
    assert len(unmatched) == 0
    unmatched = set(value.listeners['me']) ^ set(message.listeners['me'])
    assert len(unmatched) == 0
