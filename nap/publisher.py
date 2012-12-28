
from django.views.generic.base import View
from django.http import HttpResponse

import json


class Publisher(View):

    def dispatch(self, request, action='default', object_id=None, **kwargs):
        '''View dispatcher called by Django
        Add this to your url patterns like:
            ( '^foo/', include(mypublisher.urlpatterns), ),
        /                   GET: column config, POST: filtered list
        /add/               GET: form config, POST: create new instance
        /(action)/          custom action
        /(action)/(arg)/    custom action with argument (eg: /distinct/attr_name/)
        /(id)/              instance view
        /(id)/(action)/     custom action on instance
        '''
        self.action = action
        method = request.method.lower()
        if object_id is None:
            # Look for list handler
            handler = getattr(self, '%s_%s_list' % (method, action), None)
        else:
            # Look for object handler
            handler = getattr( self, '%s_%s_object' % (method, action), None )
        if handler is None:
            raise Http404
        return handler(request, object_id=object_id, **kw)

    def get_serialiser(self, request, **kwargs):
        return self.serialiser

    def get_default_list(self, request, **kwargs):
        queryset = self.get_queryset()
        serialiser = self.get_serialiser()
        return self.render_to_response(serializer.deflate_list(queryset))

    def get_default_object(self, request, object_id, **kwargs):
        # XXX Make 'pk' configurable?
        obj = self.get_queryset().get(pk=object_id)
        serialiser = self.get_serialiser()
        return self.render_to_response(serialiser.deflate_object(obj))

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(json.dumps(context),
            content_type='application/json',
        )

