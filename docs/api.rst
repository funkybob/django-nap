
APIs
====

When you have multiple Publishers collected together, it can be handy to publish them under the same path.  This is where the Api class comes in.

    api = Api('name')

    api.register(MyPublisher)
    api.register(OtherPublisher, 'friendlyname')

By default, each Publisher will be registered with the name in its "api_name" property.

Once registered, you can get a list of URL patterns to include:

    (r'^api/', include(api.patterns())),

When you add the patterns, you can optionally pass a 'flat' argument, which will omit the Api's name from the url patterns.

Also, the Api class provides an introspection view that will list all its Publishers, as well as their handlers and methods supported.

Auto-discover
-------------

Just like Django's Admin, Api supports auto-discover.

In your serialiser.py use:

    from nap import api

    ...

    api.register('apiname', Publisher....)

An Api instance with that name will be created, if it hasn't already, and put into api.APIS.  Then the publisher(s) you pass will be registered with it.

Then, in your urls.py, just add:

    from nap import api
    api.autodiscover()

Which will trigger it to import $APP.serialiser from each of your INSTALLED_APPS.  Then you can just include the urls:

    (r'^apis/', include(api.patterns()))

