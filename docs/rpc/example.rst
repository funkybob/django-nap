=====
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

