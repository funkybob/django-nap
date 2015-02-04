
from .base import Encoder

import msgpack


class MsgPackEncoder(Encoder):

    CONTENT_TYPES = ['application/x-msgpack',]

    def decode(self, data):
        return msgpack.unpackb(data)

    def encode(self, data):
        return msgpack.packb(data)
