
BasePublisher
=============

The publisher is a general purpose class for dispatching requests.  It's similar to the generic Class-Based Views in Django, but handles many views in a single class.

This pattern works well for APIs, where typically a group of views require the same functions.

The publisher recognises a small, fixed set of URL patterns, and dispatches to them to methods on the class according to a simple pattern: target, method, action.  The target is either "list" or "object", depending on if an object_id was supplied.  The method is the HTTP method, lower cased (i.e. get, put, post, delete, etc.).  And finally, the action, which defaults to 'default'.

    r'^object/(?P<object_id>[-\w]+)/(?P<action>\w+)/(?P<argument>.+)/?$'
    r'^object/(?P<object_id>[-\w]+)/(?P<action>\w+)/?$'
    r'^object/(?P<object_id>[-\w]+)/?$'
    r'^(?P<action>\w+)/(?P<argument>.+)/$'
    r'^(?P<action>\w+)/?$'
    r'^$'

Clearly this list does not permit 'object' to be an action.

Any handler should follow the same definition:

    def handler(self, request, action, object_id, \**kwargs):

Both action and object_id are passed as kwargs, so where they're not needed they can be omitted.

Every handler is expected to return a proper HttpResponse object.

Publishing
----------

In order to add a ``Publisher`` to your URL patterns, you need to include all of its own patterns.  Fortunately, it provides a handy method to make this simple:

    url(r'^myresource/', include(MyPublisher.patterns())),

Publisher
=========

The Publisher extends the BasePublisher class with some useful methods for typical REST-ful uses.

    Publisher(engine.JsonEngine, BasePublisher):

        def get_serialiser():
            Allows you to use a different ``Serialiser`` depending on the handler, or other criterial.
            The default method returns self.serialiser

        def get_object_list():
            Returns the object list for use in list handlers.

        def get_object(object_id):
            Returns the requested object, or raises Http404

        def get_page(object_list):
            Paginate the supplied object list.
            The default implementation will use the django Paginator class to paginate according to the 'offset' value in request.GET.
            The data returned will be a dict containing:
                objects:    a list of objects on this page
                meta:
                    offset: the offset of this page
                    limit: the page size
                    count: the total number of objects in the list before pagination 
                    has_next: if there is a page after this one
                    has_prev: is there is a page before this one

            If there is no page_size set, the meta dict will be empty, and objects will be the full object list.

        def get_data():
            Returns the data sent in this request.
            If the request type is specified in the ``Engine``'s supported types, it will be used to de-serialise the data.
            Otherwise, request.GET or request.POST will be returned as apporpriate for the HTTP method used.

        def render_single_object(obj, serialiser=None, \**kwargs):
            A helper function to serialise the object and create a response.
            Will call get_serialiser if serialiser is None.
            The kwargs are passed on to create_response

        def create_response(content, \**kwargs):
            Return a HttpResponse and serialiser the content using the ``Engine```.
            The default content_type will be the first in the ``Engine``'s CONTENT_TYPEs list.
            The response class can be overridden by passing response_class in kwargs.

        ## Default Handlers

        def list_get_default():
            Default list handler.
            Passes the result of ``get_object_list`` to ``get_page``, and then uses the serialiser returned by ``get_serialiser`` to deflate the object list.
            Returns the resulting data using ``create_response``.

        def object_get_default():
            Defaul object handler.
            Passes the result of ``get_object`` to ``render_single_object``


ModelPublisher
==============

The ModelPublisher implements some default handlers that are more sensible for a Model.

It includes a default ``model`` property that will return the model from the meta class of self.serialiser.  This way, by default, it will publish the model of its default Serialiser.

ModelFormMixin
==============

This class provides ``list_post_default`` and ``object_put_default`` that will use a ModelForm to validate and creat/update objects.  It uses the same methods as a standard Django FormMixin class-based view.

It also includes an ``object_delete_default`` method.
