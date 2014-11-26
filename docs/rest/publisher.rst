==========
Publishers
==========

The publisher is a general purpose class for dispatching requests.  It's similar
to the generic Class-Based Views in Django, but handles many views in a single
class.

This pattern works well for APIs, where typically a group of views require the
same functions.

.. code-block:: python

    r'^object/(?P<object_id>[-\w]+)/(?P<action>\w+)/(?P<argument>.+?)/?$'
    r'^object/(?P<object_id>[-\w]+)/(?P<action>\w+)/?$'
    r'^object/(?P<object_id>[-\w]+)/?$'
    r'^(?P<action>\w+)/(?P<argument>.+?)/$'
    r'^(?P<action>\w+)/?$'
    r'^$'

Clearly this list does not permit 'object' to be an action.

The publisher recognises a small, fixed set of URL patterns, and dispatches them
to methods on the class according to a simple pattern: target, method, action.
The target is either "list" or "object", depending on if an object_id was
supplied.  The method is the HTTP method, lower cased (i.e. get, put, post,
delete, etc.).  And finally, the action, which defaults to 'default'.

So, for example, a GET request to /foo would call the ``list_get_foo`` handler.
Whereas a POST to /object/123/nudge/ would call ``object_post_nudge``, passing
"123" as the object_id.

All handlers should follow the same definition:

.. code-block:: python

    def handler(self, request, action, object_id, **kwargs):

Both action and object_id are passed as kwargs, so where they're not needed they
can be omitted.

Like a view, every handler is expected to return a proper HttpResponse object.

Publishing
==========

In order to add a ``Publisher`` to your URL patterns, you need to include all of
its patterns.  Fortunately, it provides a handy method to make this simple:

    url(r'^myresource/', include(MyPublisher.patterns())),


Base Publisher
==============

.. class:: BasePublisher(request [,\*args] [,\**kwargs])

   .. attribute:: CSRF = True

      Determines if CSRF protection is applied to the view function used in ``patterns``

   .. attribute:: ACTION_PATTERN
   .. attribute:: OBJECT_PATTERN
   .. attribute:: ARGUMENT_PATTERN

      Used by the ``patterns`` method to control the URL patterns generated.

   .. attribute:: PATTERNS

      A list of (regex, view name) pairs to generate the URL patterns.
      They will be called with format() applied, passed the following keys:

      name
        The generated name for this Publisher.
      action
        ACTION_PATTERN
      object
        OBJECT_PATTERN
      argument
        ARGUMENT_PATTERN

   .. classmethod:: patterns(api_name=None)

      Builds a list of URL patterns for this Publisher.

      The ``api_name`` argument will be used for naming the url patterns.

   .. classmethod:: index()

      Returns details about handlers available on this publisher.

      The result will be a dict with two keys: list, and detail.

      Each item will contain a list of handlers and the HTTP verbs they accept.

   .. method::  dispatch(request, action='default', object_id=None, \**kwargs):

      Entry point used by the view function.

   .. method:: execute(handler):

      Call hook for intercepting handlers.  ``dispatch`` passes the handler
      method here to invoke.  It will call the handler, and catch any ``BaseHttpResponse``
      exceptions, returning them.

      This was originally added to make New Relic support simpler.

Custom Patterns
---------------

By overridding the patterns method, you can provide your own url patterns.

One sample is included: nap.publisher.SimplePatternsMixin

It omits the object/ portion of the object urls above, but limits object_ids to
just digits.

Alternatively, if you just want to change the regex used for each part of the
URL, you can overrid them using OBJECT_PATTERN, ACTION_PATTERN, and
ARGUMENT_PATTERN, which default to '[-\w]+', '\w+' and '.*?' respectively.

Publisher
=========

The Publisher extends the BasePublisher class with some useful methods for
typical REST-ful uses.

.. class:: Publisher

   .. attribute:: page_size

      Enable pagination and specify the default page size.
      Default: unset

   .. attribute:: max_page_size

      Limit the maximum page size.
      Default: page_size

      If a request passes an override LIMIT value, it can not exceed this.

   .. attribute:: LIMIT_PARAM

      Specifies the query parameter name used to specify the pagination size limit.
      Default: 'limit'

   .. attribute:: OFFSET_PARAM

      Specifies the query parameter name used to specify the pagination offset.
      Default: 'offset'

   .. attribute:: PAGE_PARAM

      Specifies the query parameter name used to specify the pagination page.
      Default: 'page'

   .. attribute:: response_class

      Default class to use in ``create_response``

   .. attribute:: CONTENT_TYPES

      A list of content types supported by the de/serialiser.
      Default: ['application/json', 'text/json']

      The first value in the list will be used as the content type of responses.

   .. method:: dumps(data)

      Used to serialise data.  By default calls json.dumps.

   .. method:: loads(data)

      Deserialise data.  By default calls json.loads.

   .. method:: get_serialiser()

      Called to get the ``Serialiser`` instance to use for this request.
      Default: returns self.serialiser

   .. method:: get_serialiser_kwargs()

      Used to generate extra kwargs to pass to serialiser calls (i.e.
      object_deflate, list_deflate, etc)

   .. method:: get_object_list()

      Return the raw object list for this request.
      This is Not Implemented.  You must provide this method in your Serialiser
      class.

   .. method:: get_object(object_id)

      Return the object for the given ID.
      You must provide this method in your Serialiser class.

   .. method:: filter_object_list(object_list)

      Apply filtering to an object list, returning the filtered list.
      Default: Returns the passed object_list.

   .. method:: sort_object_list(object_list)

      Apply sorting to an object list, returning the sorted list.
      Default: Returns the passed object_list.

   .. method:: get_page(object_list):

      Paginate the object_list.

      If the page_size is not defined on the Serialiser, no pagination is
      performed, and the following dict is returned:

      .. code-block:: python

         { 'meta': {}, 'objects': object_list }

      Otherwise, the object_list is paginated.  If self.PAGE_PARAM was passed,
      it will be used for the page number.  It not, and self.OFFSET_PARAM is
      supplied, the page will be determined by dividing the offset by page_size.

      The ``meta`` dict will contain:

      .. code-block:: python

         'offset': page.start_index() - 1,
         'page': page_num,
         'total_pages': paginator.num_pages,
         'limit': page_size,
         'count': paginator.count,
         'has_next': page.has_next(),
         'has_prev': page.has_previous(),


   .. method:: get_request_data()

      Returns the data sent in this request.
      If the request type is specified in ``CONTENT_TYPES`` it will be used to
      de-serialise the data.  Otherwise, request.GET or request.POST will be
      returned as apporpriate for the HTTP method used.

   .. method:: render_single_object(obj, serialiser=None, \**kwargs):

      A helper function to serialise the object and create a response, using
      self.response_class.  If ``serialiser`` is None, it will call
      ``get_serialiser``.  The kwargs will be passed on to ``create_response``

   .. method:: create_response(content, \**kwargs):

      A helper function for building ``self.response_class``.
      Passing response_class as an argument overrides the class used.

      It sets 'content_type' in kwargs to self.CONTENT_TYPES[0] if it's not set.
      Then, it passes ``content`` to ``self.dumps``, and passes that, along with
      kwargs, to build a new response_class instance, returning it.

   .. method:: list_get_default(request, \**kwargs):

      Default list handler.

      Calls `get_object_list`, `filter_object_list` and `sort_object_list`,
      then passes the list to `get_page`.  It then uses the object from
      `get_serialiser` to deflate the object list.

      Returns the resulting data using ``create_response``.

   .. method: object_get_default(request, \**kwargs):

      Defaul object handler.
      Passes the result of ``get_object`` to ``render_single_object``


Filtering and Sorting
---------------------

The Publisher class has two methods for sorting and filtering:

.. method:: filter_object_list(object_list)

.. method:: sort_object_list(object_list)

By default, these simply return the list they are passed.

Filtering and sorting are not applied by get_object_list.  This lets you apply
required filtering [site, security, user, etc] in get_object_list, and optional
filtering [query, etc] where it's wanted.  Also, ordering can be an unwanted
expense when it's not important to the use.

The default Publisher.list_get_default will pass the result of get_object_list
to filter_object_list and sort_object_list in turn before serialising.

ModelPublisher
==============

The ModelPublisher implements some default handlers that are more sensible for a
Model.

It includes a default ``model`` property that will return the model from the
meta class of self.serialiser.  This way, by default, it will publish the model
of its default Serialiser.

