__author__ = 'atrimble'


import msgpack
from io import BytesIO
from bigio.gossip_message import GossipMessage
import logging

logger = logging.getLogger(__name__)


def decode(data):
    buf = BytesIO()
    buf.write(data)
    buf.seek(0)
    unpacker = msgpack.Unpacker(buf)

    message = GossipMessage()

    ip = str(unpacker.unpack())
    ip = ip + '.'
    ip = ip + str(unpacker.unpack())
    ip = ip + '.'
    ip = ip + str(unpacker.unpack())
    ip = ip + '.'
    ip = ip + str(unpacker.unpack())

    message.ip = ip
    message.gossip_port = int(unpacker.unpack())
    message.data_port = int(unpacker.unpack())
    message.milliseconds_since_midnight = int(unpacker.unpack())
    has_public_key = unpacker.unpack()
    if has_public_key:
        message.public_key = unpacker.unpack()

    tag_map = unpacker.unpack()
    for key, value in tag_map.items():
        message.tags[key.decode('utf8')] = value.decode('utf8')

    member_array = unpacker.unpack()
    for member in member_array:
        key = str(member[0]) + '.' + str(member[1]) + '.' + str(member[2]) + '.' + str(member[3]) + ':' + str(member[4]) + ':' + str(member[5])
        message.members.append(key)

    clock_array = unpacker.unpack()
    for clock in clock_array:
        message.clock.append(clock)

    listener_map = unpacker.unpack()
    for key, value in listener_map.items():
        k = key.decode('utf8')
        message.listeners[k] = []
        for destination in value:
            message.listeners[k].append(destination.decode('utf8'))

    return message