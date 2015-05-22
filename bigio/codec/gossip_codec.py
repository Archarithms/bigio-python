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


def encode(message):
    split = message.ip.split('.')
    members = []
    listeners = dict()

    for m in message.members:
        keys = m.split(':')
        mem_ip = keys[0].split('.')
        tmp_list = []
        tmp_list.append(int(mem_ip[0]))
        tmp_list.append(int(mem_ip[1]))
        tmp_list.append(int(mem_ip[2]))
        tmp_list.append(int(mem_ip[3]))
        tmp_list.append(int(keys[1]))
        tmp_list.append(int(keys[2]))
        members.append(tmp_list)

    for key in message.listeners:
        listeners[key] = message.listeners[key]

    buf = BytesIO()
    buf.write(msgpack.packb(int(split[0])))
    buf.write(msgpack.packb(int(split[1])))
    buf.write(msgpack.packb(int(split[2])))
    buf.write(msgpack.packb(int(split[3])))
    buf.write(msgpack.packb(int(message.gossip_port)))
    buf.write(msgpack.packb(int(message.data_port)))
    buf.write(msgpack.packb(int(message.milliseconds_since_midnight)))
    if message.public_key is not None:
        buf.write(msgpack.packb(True))
        buf.write(msgpack.packb(message.public_key))
    else:
        buf.write(msgpack.packb(False))
    buf.write(msgpack.packb(message.tags))
    buf.write(msgpack.packb(members))
    buf.write(msgpack.packb(message.clock))
    buf.write(msgpack.packb(listeners))

    length = len(buf.getvalue())
    ret = BytesIO()
    ret.write(length.to_bytes(2, byteorder='big'))
    ret.write(buf.getvalue())

    return ret.getvalue()
