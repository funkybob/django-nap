from __future__ import unicode_literals

import inspect
from collections import defaultdict

from django.conf.urls import url
from django.core.paginator import EmptyPage, Paginator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from .. import http
from ..utils import JsonMixin


def accepts(*verbs):
    '''Annotate a method with the HTTP verbs it accepts, and enforce it.'''
    def _inner(method):
        setattr(method, '_accepts', verbs)
        return method_decorator(
            require_http_methods([x.upper() for x in verbs])
        )(method)
    return _inner


class BasePublisher(object):
    CSRF = True

    ACTION_PATTERN = r'\w+'
    OBJECT_PATTERN = r'[-\w]+'
    ARGUMENT_PATTERN = r'.+?'

    PATTERNS = [
        (r'^object/(?P<object_id>{object})/(?P<action>{action})/(?P<argument>{argument})/?$', '{name}_object_action_arg'),
        (r'^object/(?P<object_id>{object})/(?P<action>{action})/?$', '{name}_object_action'),
        (r'^object/(?P<object_id>{object})/?$', '{name}_object_default'),
        (r'^(?P<action>{action})/(?P<argument>{argument})/?$', '{name}_list_action_arg'),
        (r'^(?P<action>{action})/?$', '{name}_list_action'),
        (r'^$', '{name}_list_default'),
    ]

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    @classmethod
    def build_view(cls):
        '''Builds the view function for this publisher.'''
        def view(request, *args, **kwargs):
            '''A wrapper view to instantiate and dispatch'''
            self = cls(request, *args, **kwargs)
            return self.dispatch(request, **kwargs)

        if cls.CSRF:
            view = ensure_csrf_cookie(view)
        else:
            view = csrf_exempt(view)
        return view

    @classmethod
    def patterns(cls, api_name=None):
        '''
        Yields a list of URL patterns for this Publisher.

        Add this to your url patterns like:
            ('^foo/', include(mypublisher.patterns()),),
        '''
        view = cls.build_view()

        name = getattr(cls, 'api_name', cls.__name__.lower())
        if api_name:
            name = '%s_%s' % (api_name, name)

        fmt = {
            'name': name,
            'object': cls.OBJECT_PATTERN,
            'action': cls.ACTION_PATTERN,
            'argument': cls.ARGUMENT_PATTERN,
        }

        return [
            url(url_pattern.format(**fmt), view, name=view_name.format(**fmt))
            for url_pattern, view_name in cls.PATTERNS
        ]

    def dispatch(self, request, action='default', object_id=None, **kwargs):
        '''View dispatcher called by Django'''
        self.action = action
        self.object_id = object_id
        method = request.method.lower()
        self.mode = prefix = 'object' if object_id else 'list'
        handler = getattr(self, '%s_%s_%s' % (prefix, method, action), None)
        if handler is None:
            # See if there's a method agnostic handler
            handler = getattr(self, '%s_%s' % (prefix, action), None)
        if handler is None:
            return http.NotFound()
        # Do we need to pass any of this?
        return self.execute(handler)

    def execute(self, handler):
        '''This allows wrapping calls to handler functions'''
        try:
            return handler(self.request,
                action=self.action,
                object_id=self.object_id,
            )
        except http.BaseHttpResponse as response:
            return response

    @classmethod
    def index(cls):
        '''Return details about which handlers exist on this publisher.'''
        list_handlers = defaultdict(list)
        object_handlers = defaultdict(list)
        for name, fnc in inspect.getmembers(cls, inspect.ismethod):
            parts = name.split('_')

            if parts[0] == 'list':
                if len(parts) == 2:
                    list_handlers[parts[1]].extend(getattr(fnc, '_accepts', ['ALL']))
                else:
                    list_handlers[parts[2]].append(parts[1])

            elif parts[0] == 'object':
                if len(parts) == 2:
                    object_handlers[parts[1]].extend(getattr(fnc, '_accepts', ['ALL']))
                else:
                    object_handlers[parts[2]].append(parts[1])

        return {
            'list': list_handlers,
            'object': object_handlers,
        }


class SimplePatternsMixin(object):
    '''
    A "flatter" set of url patterns for when your object IDs are numbers only.
    '''

    ACTION_PATTERN = r'\w+'
    OBJECT_PATTERN = r'\d+'
    ARGUMENT_PATTERN = r'.+?'

    PATTERNS = [
        (r'^(?P<object_id>{object})/(?P<action>{action})/(?P<argument>{argument})/?$', '{name}_object_action_arg'),
        (r'^(?P<object_id>{object})/(?P<action>{action})/?$', '{name}_object_action'),
        (r'^(?P<object_id>{object})/?$', '{name}_object_default'),
        (r'^(?P<action>{action})/(?P<argument>{argument})/?$', '{name}_list_action_arg'),
        (r'^(?P<action>{action})/?$', '{name}_list_action'),
        (r'^$', '{name}_list_default'),
    ]


class Publisher(JsonMixin, BasePublisher):
    '''Default API-style publisher'''
    LIMIT_PARAM = 'limit'
    OFFSET_PARAM = 'offset'
    PAGE_PARAM = 'page'

    response_class = http.HttpResponse

    # De/Serialising
    # Which content types will we attempt to parse?
    # The first in the list will be used for responses.

    # Hooks for controlling which serialiser to use

    def get_serialiser(self):
        '''Return the serialiser instance to use for this request'''
        return self.serialiser

    def get_serialiser_kwargs(self):
        '''Allow passing of extra kwargs to serialiser calls'''
        return {
            'publisher': self,
        }

    # Object access

    def get_object_list(self):  # pragma: no cover
        '''Return the object list appropriate for this request'''
        raise NotImplementedError

    def get_object(self, object_id):  # pragma: no cover
        '''Return the object for the given id'''
        raise NotImplementedError

    # List filtering and sorting

    def filter_object_list(self, object_list):
        '''Hook to allow custom filtering of object lists'''
        return object_list

    def sort_object_list(self, object_list):
        '''Hook to allow custom sorting of object lists'''
        return object_list

    # Pagination
    def get_page(self, object_list):
        '''
        Return a paginated object list, along with some metadata

        If self.page_size is not None, pagination is enabled.

        The page_size can be overridden by passing it in the requst, but it is
        limited to 1 < page_size < max_page_size.

        max_page_size defaults to self.page_size.

        If a page_num is passed, it is fed to regular Django pagination
        If an offset is passed, page_num is derived from it by dividing it by
        page_size.

        '''
        page_size = getattr(self, 'page_size', None)
        if page_size is None:
            return {
                'meta': {},
                'objects': object_list,
            }
        max_page_size = getattr(self, 'max_page_size', page_size)

        try:
            page_size = int(self.request.GET.get(self.LIMIT_PARAM, page_size))
        except ValueError:
            raise http.NotFound('Invalid page size')
        page_size = max(1, min(page_size, max_page_size))

        page_num = 0
        try:
            page_num = int(self.request.GET[self.PAGE_PARAM])
        except ValueError:
            # Bad page - default to 0
            pass
        except KeyError:
            try:
                offset = int(self.request.GET[self.OFFSET_PARAM])
            except (ValueError, KeyError):
                pass
            else:
                page_num = offset // page_size

        paginator = Paginator(object_list, page_size, allow_empty_first_page=True)
        try:
            page = paginator.page(page_num + 1)
        except EmptyPage:
            raise http.NotFound()
        return {
            'meta': {
                'offset': page.start_index() - 1,
                'page': page_num,
                'total_pages': paginator.num_pages,
                'limit': page_size,
                'count': paginator.count,
                'has_next': page.has_next(),
                'has_prev': page.has_previous(),
            },
            'objects': page.object_list,
        }

    # Response helpers

    def create_response(self, content, **response_kwargs):
        '''Return a response, serialising the content'''
        response_class = response_kwargs.pop('response_class', self.response_class)
        response_kwargs.setdefault('content_type', self.CONTENT_TYPES[0])
        return response_class(self.dumps(content), **response_kwargs)

    def render_single_object(self, obj, serialiser=None, **response_kwargs):
        '''Helper to return a single object instance serialised.'''
        if serialiser is None:
            serialiser = self.get_serialiser()
        serialiser_kwargs = response_kwargs.pop('serialiser_kwargs', None)
        if serialiser_kwargs is None:
            serialiser_kwargs = self.get_serialiser_kwargs()
        data = serialiser.object_deflate(obj, **serialiser_kwargs)
        return self.create_response(data, **response_kwargs)

    # Default handlers

    def list_get_default(self, request, **kwargs):
        object_list = self.get_object_list()
        object_list = self.filter_object_list(object_list)
        object_list = self.sort_object_list(object_list)

        data = self.get_page(object_list)

        serialiser = self.get_serialiser()
        serialiser_kwargs = self.get_serialiser_kwargs()
        data['objects'] = serialiser.list_deflate(data['objects'], **serialiser_kwargs)
        return self.create_response(data)

    def object_get_default(self, request, object_id, **kwargs):
        '''Default object GET handler -- get object'''
        obj = self.get_object(object_id)
        return self.render_single_object(obj)
