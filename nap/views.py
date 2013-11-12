from __future__ import unicode_literals

from .publisher import Publisher, SimplePatternsMixin

from django.template.response import TemplateResponse

class ViewPublisher(SimplePatternsMixin, Publisher):
    '''
    A Publisher for non-API views.

    Replaces create_response with a wrapper around TemplateResponse.
    '''

    def create_response(self, content, template, **response_kwargs):
        '''Return a response serialising the content'''
        return TemplateResponse(self.request, template, content, **response_kwargs)
