====
APIs
====

When you have multiple Publishers collected together, it can be handy to
publish them under the same path.  This is where the Api class comes in.

.. code-block:: python

    api = Api('name')

    api.register(MyPublisher)
    api.register(OtherPublisher, 'friendlyname')

If not overridden by being passed in the call to register, the Publisher will
be registered with the name in its ``api_name`` property.  This is used as the
root of its URL within the Api.

Once registered, you can get a list of URL patterns to include:

.. code-block:: python

    (r'^api/', include(api.patterns())),

When you add the patterns, you can optionally pass a 'flat' argument, which
will omit the Api's name from the url patterns.

Also, the Api class provides an introspection view that will list all its
Publishers, as well as their handlers and methods supported.

Auto-discover
-------------

Just like Django's Admin, Api supports auto-discover.

In your publishers.py use:

.. code-block:: python

    from nap import api

    ...

    api.register('apiname', Publisher,....)

If you're only registering a single Publisher, you can use api.register as a decorator.

.. code-block:: python

   @api.register('apiname')
   class JoyPublisher(Publisher):

An Api instance with that name will be created, if it hasn't already, and put
into api.APIS.  Then the publisher(s) you pass will be registered with it.

.. note::

   The publisher will be registered as the lower-cased version of its class
   name.  You can control this by setting an ``api_name`` property.

Then, in your urls.py, just add:

.. code-block:: python

    from nap import api
    api.autodiscover()

Which will trigger it to import $APP.serialiser from each of your
INSTALLED_APPS.  Then you can just include the urls:

.. code-block:: python

    (r'^apis/', include(api.patterns()))

