from __future__ import unicode_literals

from django.db import transaction

from .. import http
from ..shortcuts import get_object_or_404
from .publisher import Publisher


class ModelPublisher(Publisher):
    '''A Publisher with useful methods to publish Models'''

    @property
    def model(self):
        '''By default, we try to get the model from our serialiser'''
        # XXX Should this call get_serialiser?
        return self.serialiser._meta.model

    # Auto-build serialiser from model class?

    def get_object_list(self):
        return self.model.objects.all()

    def get_object(self, object_id):
        return get_object_or_404(self.get_object_list(), pk=object_id)

    def list_post_default(self, request, **kwargs):
        data = self.get_request_data()

        serialiser = self.get_serialiser()
        serialiser_kwargs = self.get_serialiser_kwargs()
        try:
            with transaction.atomic():
                obj = serialiser.object_inflate(data, **serialiser_kwargs)
        except ValueError as e:
            return http.BadRequest(str(e))
        return self.render_single_object(obj, serialiser)
