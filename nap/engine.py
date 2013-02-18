
import json


class Engine(object):
    # The list of content types we match
    CONTENT_TYPES = []
    def dumps(self, data): # pragma: no cover
        '''How to serialiser an object'''
        raise NotImplementedError
    
    def loads(self, data): # pragma: no cover
        '''How to deserialise a string'''
        raise NotImplementedError


class JsonEngine(Engine):
    CONTENT_TYPES = ['application/json',]
    def dumps(self, data):
        return json.dumps(data)
    def loads(self, data):
        return json.loads(data)


try:
    import msgpack
except ImportError:
    pass
else:
    class MsgPackEngine(Engine):
        CONTENT_TYPES = ['application/x-msgpack',]
        def dumps(self, data):
            return msgpack.dumps(data)
        def loads(self, data):
            return msgpack.loads(data)
