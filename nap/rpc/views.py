
from cgi import parse_header
import json

from django.http import HttpResponse
from django.core.handlers.wsgi import ISO_8859_1
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import View


RPC_MARKER = '_rpc'


class RPCMixin(object):
    '''Mix in to a standard View to provide RPC actions'''

    def dispatch(self, request, *args, **kwargs):
        method = request.META.get('HTTP_X_RPC_ACTION', None)
        if request.method != 'POST' or method is None:
            return super(RPCMixin, self).dispatch(request, *args, **kwargs)

        func = getattr(self, method, None)
        if not getattr(func, RPC_MARKER, False):
            return HttpResponse(status=412)

        data = self.get_request_data(request)

        resp = self.execute(func, data)
        serialised_resp = json.dumps(resp, cls=DjangoJSONEncoder)

        return HttpResponse(serialised_resp, content_type='application/json')

    def execute(self, handler, data):
        '''Helpful hook to ease wrapping the handler'''
        return handler(**data)

    def get_request_data(self, default=None):
        '''Retrieve data from request'''
        c_type, _ = parse_header(self.request.META.get('CONTENT_TYPE', ''))
        if c_type in ['application/json', 'text/json']:
            if not self.request.body:
                return default
            return json.loads(self.request.body.decode(
                getattr(self.request, 'encoding', ISO_8859_1)
            ))
        return self.request.POST


class RPCView(RPCMixin, View):
    '''courtesy class to avoid having to mix it yourself.'''
    pass


def method(view):
    '''Mark a view as accessible via RPC'''
    setattr(view, RPC_MARKER, True)
    return view
