__author__ = 'atrimble'

import msgpack
from io import BytesIO
import logging
import inspect
import re
import types

logger = logging.getLogger(__name__)


def encode(message):
    buf = BytesIO()

    for tup in inspect.getmembers(message):
        if not re.match('^__', tup[0]):
            buf.write(msgpack.packb(tup[1], use_bin_type=True))

    return buf.getvalue()


def decode(data, message_type):
    if isinstance(message_type, types.ModuleType):
        message = message_type
    elif isinstance(message_type, object):
        message = message_type()

    buf = BytesIO(data)
    unpacker = msgpack.Unpacker(buf, encoding='utf8')

    for tup in inspect.getmembers(message):
        if not re.match('^__', tup[0]):
            try:
                value = unpacker.unpack()

                if isinstance(message.__dict__[tup[0]], str):
                    pass
                elif isinstance(message.__dict__[tup[0]], dict):
                    pass
                else:
                    pass

                setattr(message, tup[0], value)
            except msgpack.exceptions.OutOfData as err:
                logger.error('Ran out of data on "' + str(tup[0]) + '"')

    return message

