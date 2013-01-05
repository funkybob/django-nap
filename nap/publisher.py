
from django.conf.urls import url
from django.core.paginator import Paginator

from . import http

class Publisher(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    # XXX Need some names/labels to build url pattern names?
    @classmethod
    def patterns(cls):
        '''
        Add this to your url patterns like:
            ( '^foo/', include(mypublisher.patterns()), ),
        /                       default object list
        /(action)/              list operation
        /object/(id)/           instance view
        /object/(id)/(action)/  custom action on instance
        '''
        def view(request, *args, **kwargs):
            '''A wrapper view to instanciate and dispatch'''
            self = cls(request, *args, **kwargs)
            return self.dispatch(request, *args, **kwargs)

        return [
            url(r'^object/(?P<object_id>[-\w]+)/(?P<action>\w+)/?$', view),
            url(r'^object/(?P<object_id>[-\w]+)/?$',                 view),
            url(r'^(?P<action>\w+)/?$',                           view),
            url(r'^$',                                            view),
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
            },
            'objects': page.object_list,
        }

    def get_data(self):
        '''Retrieve data from request'''
        if self.request.META['CONTENT_TYPE'] in ['application/json',]:
            if not self.request.body:
                return None
            return http.loads(self.request.body)
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

    def render_single_object(self, obj, serialiser=None):
        if serialiser is None:
            serialiser = self.get_serialiser()
        data = serialiser.deflate_object(obj, publisher=self)
        return http.JsonResponse(data)

    def create_response(self, context, **response_kwargs):
        return http.JsonResponse(context)

class ModelPublisher(Publisher):

    # Auto-build serialiser from model class?

    def get_object_list(self):
        return self.model.objects.all()

    def get_object(self, object_id):
        return self.get_object_list().get(pk=object_id)

