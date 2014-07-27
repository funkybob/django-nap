===
RPC
===

The RPC View allows your application to provide APIs that don't mate up with REST patterns.

How does it work?
=================

Any POST request with a ``X-RPC-Action`` header will be intercepted and treated as a RPC request.  If there is a method on the view class which matches the name in the header, and it's been decorated as ``@rpc`` accessible, the request data will be parsed, passed as keyword arguments to the method, and the result JSON encoded and returned.

Usage
=====

.. code-block:: python

   class MathView(RPCView):

       @rpc
       def add(self, a, b):
           return a + b


.. code-block:: python

   url(r'^rpc/$', MathView.as_view(), name'rpc-view'),

.. code-block:: javascript

   $.ajax({
        type: 'POST',
        url: '/rpc/',
        data: {a: 5, b: 10}
        headers: {
            'X-RPC-Action': method,
            'Content-Type': 'application/json'
        },
        success: function (data) { alert(data); }
    });

API
===

.. class:: RPCMixin

   .. method:: dispatch(request, \*args, \**kwargs)

   .. method:: execute(handler, data)

      Dispacth will pass the handler method and data to this method to invoke it.

      This allows all calls to intercepted for whatever reason you feel, including helping NewRelic report correctly.

   .. method:: get_request_data(default=None)

      Helper method to decode the request data.

      Default implementation is identical to ``BasePublisher``, which will decode JSON if the content type is 'application/json' or 'text/json', else request.POST


.. class:: RPCView

   Simply RPCMixin alreacy mixed with ``django.views.generic.View``


.. method:: rpc

   A decorator for RPC endpoint methods.  Without this, the method is not accessible.
