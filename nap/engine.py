
import json
try:
    import msgpack
except ImportError:
    pass

from decimal import Decimal
from datetime import date, datetime, time

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, (datetime, time,)):
            return obj.replace(microsecond=0).isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        return super(JsonEncoder, self).default(obj)

class Engine(object):
    # The list of content types we match
    CONTENT_TYPES = []
    def dumps(self, data):
        '''How to serialiser an object'''
        raise NotImplementedError
    
    def loads(self, data):
        '''How to deserialise a string'''
        raise NotImplementedError

class JsonEngine(Engine):
    CONTENT_TYPES = ['application/json',]
    def dumps(self, data):
        return json.dumps(data, cls=JsonEncoder)
    def loads(self, data):
        return json.loads(data)

class MsgPackEngine(Engine):
    CONTENT_TYPES = ['application/x-msgpack',]
    def dumps(self, data):
        return msgpack.dumps(data)
    def loads(self, data):
        return msgpack.loads(data)
