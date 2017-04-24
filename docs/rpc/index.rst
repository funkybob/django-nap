===
RPC
===

The RPC View allows your application to provide APIs that don't mate up with
REST patterns.

Overview
========

Any POST request with a ``X-RPC-Action`` header will be intercepted and treated
as a RPC request.  If there is a method on the view class which matches the name
in the header, and it's been decorated as ``@method`` accessible, the request
data will be parsed, passed as keyword arguments to the method, and the result
JSON encoded and returned.


Usage
=====

Define a View using the Mixin:

.. code-block:: python

   from nap import rpc

   class MathView(rpc.RPCView):

       @rpc.method
       def add(self, a, b):
           return a + b

Add it to your URL patterns:

.. code-block:: python

   url(r'^rpc/$', MathView.as_view(), name'rpc-view'),

Invoke it from Javascript:

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

