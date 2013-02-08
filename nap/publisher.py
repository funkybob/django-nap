
from django.conf.urls import url
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django import http

from . import engine

class Publisher(engine.JsonEngine):

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    # XXX Need some names/labels to build url pattern names?
    @classmethod
    def patterns(cls, api_name=None):
        '''
        Add this to your url patterns like:
            ( '^foo/', include(mypublisher.patterns()), ),
        /                       default object list
        /(action)/              list operation
        /(action)/(option)/     list operation with extra argument
        /object/(id)/           instance view
        /object/(id)/(action)/  custom action on instance
        '''
        def view(request, *args, **kwargs):
            '''A wrapper view to instanciate and dispatch'''
            self = cls(request, *args, **kwargs)
            return self.dispatch(request, *args, **kwargs)

        if api_name:
            name = '_'.join([api_name, cls.api_name])
        else:
            name = self.api_name

        return [
            url(r'^object/(?P<object_id>[-\w]+)/(?P<action>\w+)/(?P<argument>.+)/?$',
                view,
                name='%s_object_action_arg' % name,
            ),
            url(r'^object/(?P<object_id>[-\w]+)/(?P<action>\w+)/?$',
                view,
                name='%s_object_action' % name,
            ),
            url(r'^object/(?P<object_id>[-\w]+)/?$',
                view,
                name='%s_object_default' % name,
            ),
            url(r'^(?P<action>\w+)/(?P<argument>.+)/$',
                view,
                name='%s_list_action_arg' % name,
            ),
            url(r'^(?P<action>\w+)/?$',
                view,
                name='%s_list_action' % name,
            ),
            url(r'^$',
                view,
                name='%s_list_default' % name,
            ),
        ]

    def dispatch(self, request, action='default', object_id=None, **kwargs):
        '''View dispatcher called by Django'''
        self.action = action
        method = request.method.lower()
        prefix = 'object' if object_id else 'list'
        handler = getattr(self, '_'.join([prefix, method, action]), None)
        if handler is None:
            handler = getattr(self, '_'.join([prefix, action]), None)
        # See if there's a method agnostic handler
        if handler is None:
            raise http.Http404
        # Do we need to pass any of this?
        return handler(request, action=action, object_id=object_id, **kwargs)

    def get_serialiser(self):
        return self.serialiser

    def get_object_list(self):
        raise NotImplementedError

    def get_object(self, object_id):
        raise NotImplementedError

    def get_page(self, object_list):
        page_size = getattr(self, 'page_size', None)
        if not page_size:
            return {
                'meta': {},
                'objects': object_list,
            }
        paginator = Paginator(object_list, page_size)
        offset = int(self.request.GET.get('offset', 0))
        page_num = offset // page_size
        page = paginator.page(page_num + 1)
        return {
            'meta': {
                'offset': page.start_index() - 1,
                'limit': page_size,
                'count': paginator.count,
                'has_next': page.has_next(),
                'has_prev': page.has_previous(),
            },
            'objects': page.object_list,
        }

    def get_data(self):
        '''Retrieve data from request'''
        if self.request.META['CONTENT_TYPE'] in self.CONTENT_TYPES:
            if not self.request.body:
                return None
            return self.loads(self.request.body)
        if self.request.method == 'GET':
            return self.request.GET
        return self.request.POST

    def list_get_default(self, request, **kwargs):
        object_list = self.get_object_list()
        serialiser = self.get_serialiser()
        data = self.get_page(object_list)
        data['objects'] = serialiser.deflate_list(data['objects'], publisher=self)
        return self.create_response(data)

    def list_post_default(self, request, object_id=None, **kwargs):
        '''Default list POST handler -- create object'''

    def object_get_default(self, request, object_id, **kwargs):
        '''Default object GET handler -- get object'''
        obj = self.get_object(object_id)
        serialiser = self.get_serialiser()
        return self.render_single_object(obj, serialiser)

    def object_put_default(self, request, object_id, **kwargs):
        '''Default object PUT handler -- update object'''
        obj = self.get_object(object_id)
        serialiser = self.get_serialiser()
        obj = serialiser.inflate_object(self.get_data(), obj)
        return self.render_single_object(obj, serialiser)

    def render_single_object(self, obj, serialiser=None, **response_kwargs):
        if serialiser is None:
            serialiser = self.get_serialiser()
        data = serialiser.deflate_object(obj, publisher=self)
        return self.create_response(data, **response_kwargs)

    def create_response(self, content, **response_kwargs):
        response_class = response_kwargs.pop('response_class', http.HttpResponse)
        return response_class(self.dumps(content), **response_kwargs)


class ModelPublisher(Publisher):
    @property
    def model(self):
        '''By default, we try to get the model from out serialiser'''
        return self.serialiser._meta.model

    # Auto-build serialiser from model class?

    def get_object_list(self):
        return self.model.objects.all()

    def get_object(self, object_id):
        return get_object_or_404(self.get_object_list(), pk=object_id)

