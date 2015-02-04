
import json

from .base import Encoder

class JsonEncoder(Encoder):

    CONTENT_TYPES = ['application/json', 'text/json']

    def decode(self, data):
        return json.loads(data)

    def encode(self, data):
        return json.dumps(data)
