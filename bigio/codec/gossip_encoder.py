__author__ = 'atrimble'


import msgpack
from io import BytesIO
import logging

logger = logging.getLogger(__name__)


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
