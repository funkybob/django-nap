
from django.conf.urls import url
from django.core.paginator import Paginator
from django.views.generic.base import View
from django.http import HttpResponse, Http404

import json


class Publisher(View):
    @classmethod
    def patterns(cls, **kwargs):
        view = cls.as_view(**kwargs)
        return [
            url(r'^(?P<object_id>\d+)/(?P<action>\w+)/?$', view, ),
            url(r'^(?P<object_id>\d+)/?$',                 view, ),
            url(r'^(?P<action>\w+)/(?P<arg>\w+)/?$',       view, ),
            url(r'^(?P<action>\w+)/?$',                    view, ),
            url(r'^$',                                     view, ),
        ]

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
        self.request = request  # Shouldn't the as_view wrapper do this?
        method = request.method.lower()
        if object_id is None:
            # Look for list handler
            handler = getattr(self, 'do_%s_%s_list' % (method, action), None)
        else:
            # Look for object handler
            handler = getattr( self, 'do_%s_%s_object' % (method, action), None )
        if handler is None:
            raise Http404
        return handler(request, object_id=object_id, **kwargs)

    def get_serialiser(self, request, **kwargs):
        return self.serialiser

    def get_object_list(self):
        raise NotImplementedError

    def get_object(self, object_id):
        raise NotImplementedError

    def get_page(self, object_list):
        page_size = getattr(self, 'page_size', None)
        if page_size is None:
            return {
                'meta': {},
                'objects': object_list,
            }
        paginator = Paginator(object_list, page_size)
        offset = int(self.request.GET.get('offset', 0))
        page_num = offset // page_size
        page = paginator.page(page_num or 1)
        return {
            'meta': {
                'offset': page.start_index(),
                'limit': page_size,
                'count': paginator.count,
            },
            'objects': page.object_list,
        }

    def do_get_default_list(self, request, **kwargs):
        object_list = self.get_object_list()
        serialiser = self.get_serialiser(request, **kwargs)
        data = self.get_page(object_list)
        data['objects'] = serialiser.deflate_list(data['objects'])
        return self.render_to_response(data)

    def do_get_default_object(self, request, object_id, **kwargs):
        # XXX Make 'pk' configurable?
        obj = self.get_object(object_id)
        serialiser = self.get_serialiser(request, **kwargs)
        return self.render_to_response(serialiser.deflate_object(obj))

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(json.dumps(context),
            content_type='application/json',
        )

class ModelPublisher(Publisher):

    def get_object_list(self):
        return self.model.objects.all()

    def get_object(self, object_id):
        return self.get_object_list().get(pk=object_id)

