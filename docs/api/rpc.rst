========
RPCMixin
========

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

