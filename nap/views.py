from __future__ import unicode_literals

from .publisher import Publisher, SimplePatternsMixin
from .models import ModelPublisher

from django.template.response import TemplateResponse

class ViewPublisherMixin(object):
    '''
    A Publisher for non-API views.

    Replaces create_response with a wrapper around TemplateResponse.
    '''

    def create_response(self, content, template, **response_kwargs):
        '''Return a response serialising the content'''
        return TemplateResponse(self.request, template, content,
            **response_kwargs
        )

class ViewPublisher(SimplePatternsMixin, Publisher):
    pass

class ModelViewPublisher(SimplePatternsMixin, ModelPublisher):
    model = None
