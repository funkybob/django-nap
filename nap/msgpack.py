
from django.http import HttpResponse
import msgpack

class MsgPackRepsponse(HttpResponse):
    def __init__(self, content, *args, **kwargs):
        kwargs.setdefault('content_type', 'application/msgpack')
        super(MsgPackResponse, self).__init__(content, *args, **kwargs)

