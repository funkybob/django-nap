from __future__ import unicode_literals

from .. import http


class SerialisedResponseMixin(object):
    '''
    Passes context data through a
    '''
    content_type = 'application/json'
    response_class = http.JsonResponse

    def render_to_response(self, context, **response_kwargs):
        response_class = response_kwargs.pop('response_class', self.response_class)
        return response_class(context, **response_kwargs)

# TODO Add mixins for CRUD stages to process data through serialisers
