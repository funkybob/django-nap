from __future__ import unicode_literals

from .publisher import Publisher, SimplePatternsMixin
from .models import ModelPublisher

from django.template.response import TemplateResponse

class ViewPublisherMixin(object):
    '''
    A Publisher for non-API views.

    Replaces create_response with a wrapper around TemplateResponse.
    '''
    api_name = None

    def get_template_name(self):
        '''Return the template name to use for this view.'''
        return '%s/%s_%s.html' % (
            self.api_name or self.model._meta.app_label,
            self.model._meta.model_name,
            self.action,
        )

    def create_response(self, content, **response_kwargs):
        '''Return a response serialising the content'''
        template = response_kwargs.pop('template', None)
        if not template:
            template = self.get_template_names()
        return TemplateResponse(self.request, template, content,
            **response_kwargs
        )

class ViewPublisher(SimplePatternsMixin, Publisher):
    pass

class ModelViewPublisher(SimplePatternsMixin, ModelPublisher):
    model = None
