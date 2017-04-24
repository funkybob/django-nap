
import inspect
import json

from django.views.generic import View

from nap import http
from nap.utils import JsonMixin

RPC_MARKER = '_rpc'


def method(view):
    '''Mark a view as accessible via RPC'''
    setattr(view, RPC_MARKER, True)
    return view


def is_rpc_method(m):
    '''Helper for checking if something is marked as a pubishable method.'''
    return getattr(m, RPC_MARKER, False)


class RPCMixin(JsonMixin):
    '''Mix in to a standard View to provide RPC actions'''
    permit_introspect = False

    def dispatch(self, request, *args, **kwargs):
        '''
        Check if this is a POST and has the X-RPC-Action header.

        If so, dispatch the request to the method, if it exists and is
        publishable.

        Otherwise behaves as normal.
        '''
        method = request.META.get('HTTP_X_RPC_ACTION', None)
        if request.method != 'POST' or method is None:
            return super(RPCMixin, self).dispatch(request, *args, **kwargs)

        func = getattr(self, method, None)
        if not is_rpc_method(func):
            return http.PreconditionFailed()

        try:
            data = self.get_request_data({})
            # Ensure data is valid for passing as **kwargs
            (lambda **kwargs: None)(**data)
        except (ValueError, TypeError):
            return http.BadRequest()

        resp = self.execute(func, data)

        return http.JsonResponse(resp)

    def options(self, request, *args, **kwargs):
        '''
        Default OPTIONS handler.

        Returns introspection data.
        '''
        response = super(RPCMixin, self).options(request, *args, **kwargs)
        if self.permit_introspect:
            response['Content-Type'] = 'application/json'
            response.write(json.dumps(self._introspect()))
        return response

    def _introspect(self):
        '''
        Provides a list of methods available on this view.
        '''
        methods = {}
        for name, prop in inspect.getmembers(self, is_rpc_method):
            argspec = inspect.getargspec(prop)
            methods[name] = {
                'args': argspec.args[1:],
                'doc': inspect.getdoc(prop),
                'defaults': argspec.defaults,
            }
        return methods

    def execute(self, handler, data):
        '''Helpful hook to ease wrapping the handler'''
        return handler(**data)


class RPCView(RPCMixin, View):
    '''Courtesy class to avoid having to mix it yourself.'''
    pass
