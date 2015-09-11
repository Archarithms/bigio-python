__author__ = 'atrimble'


import msgpack
from io import BytesIO
import logging
from bigio.envelope import Envelope
from bigio.util import utils
from bigio.codec import generic_codec
import importlib

logger = logging.getLogger(__name__)


def encode(envelope):
    buf = BytesIO()

    keys = envelope.sender_key.split(':')
    ip = keys[0].split('.')

    buf.write(msgpack.packb(int(ip[0])))
    buf.write(msgpack.packb(int(ip[1])))
    buf.write(msgpack.packb(int(ip[2])))
    buf.write(msgpack.packb(int(ip[3])))
    buf.write(msgpack.packb(int(keys[1])))
    buf.write(msgpack.packb(int(keys[2])))

    if envelope.encrypted:
        buf.write(msgpack.packb(True))
        buf.write(msgpack.packb(envelope.key))
    else:
        buf.write(msgpack.packb(False))

    buf.write(msgpack.packb(int(envelope.execute_time)))
    buf.write(msgpack.packb(int(envelope.milliseconds_since_midnight)))
    buf.write(msgpack.packb(str(envelope.topic)))
    buf.write(msgpack.packb(str(envelope.partition)))
    buf.write(msgpack.packb(str(envelope.type)))

    m = generic_codec.encode(envelope.message)
    buf.write(msgpack.packb(m))

    length = len(buf.getvalue())
    ret = BytesIO()
    ret.write(length.to_bytes(2, byteorder='big'))
    ret.write(buf.getvalue())

    return ret.getvalue()


def decode(data):
    print(data)

    buf = BytesIO()
    buf.write(data)
    buf.seek(0)
    unpacker = msgpack.Unpacker(buf)

    ip = str(unpacker.unpack()) + '.' + str(unpacker.unpack()) + '.' + str(unpacker.unpack()) + '.' + str(unpacker.unpack())

    envelope = Envelope()
    envelope.sender_key = utils.get_key(ip=ip, gossip_port=int(unpacker.unpack()), data_port=int(unpacker.unpack()))
    envelope.encrypted = unpacker.unpack()
    if envelope.encrypted:
        envelope.key = unpacker.unpack().decode('utf8')
    else:
        envelope.key = None
    envelope.execute_time = int(unpacker.unpack())
    envelope.milliseconds_since_midnight = int(unpacker.unpack())
    envelope.topic = unpacker.unpack().decode('utf8')
    envelope.partition = unpacker.unpack().decode('utf8')
    envelope.type = unpacker.unpack().decode('utf8')
    envelope.payload = unpacker.unpack()

    spl = envelope.type.split('.')
    module = '.'.join(spl[0:-1])
    name = spl[-1]
    try:
        cl = class_for_name(module, name)
        envelope.message = generic_codec.decode(envelope.payload, cl)
    except ImportError:
        logger.warn('Could not locate message type "' + module + '.' + name + '"')

    return envelope


def class_for_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c
