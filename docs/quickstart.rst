Quick Start
===========

1. Create a Serialiser for your Model in serialisers.py

.. code-block:: python

    from nap import serialiser
    from myapp.models import MyModel

    class MyModelSerialiser(serialiser.ModelSerialiser):
        class Meta:
            model = MyModel
            exclude = ['user',]

2. Create a Publisher in publishers.py, and register it.

.. code-block:: python

    from nap import rest
    from myapp.serialisers import MyModelSerialiser

    class MyModelPublisher(rest.ModelPublisher):
        serialiser = MyModelSerialiser()

    rest.api.register('api', MyModelPublisher)

3. Auto-discover publishers, and add your APIs to your URLs:

.. code-block:: python

    from nap import rest

    rest.api.autodiscover()

    urlpatterns('',
        (r'', include(rest.api.patterns())
        ...
    )

