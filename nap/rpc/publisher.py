
from django.conf.urls import url

from nap.publisher import Publisher
from nap import http

class RpcPublisher(Publisher):
    '''
    RPC Style Publisher.

    Single URL endpoint, determines handler based on X-RPC-Action header and
    HTTP method.
    '''

    @classmethod
    def patterns(cls, api_name=None):
        view = cls.build_view()

        if api_name:
            name = '%s_%s' % (api_name, cls.api_name)
        else:
            name = cls.api_name

        return [
            url(r'^$', view, name='%s_endpoint' % name),
        ]

    def dispatch(self, request):
        self.action = request.HTTP['X-RPC-ACTION']
        try:
            handler = getattr(self, 'do_%s' % self.action, None)
        except AttributeError:
            return http.NotFound()

        return self.execute(handler)
