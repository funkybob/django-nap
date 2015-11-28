=======
RPC API
=======

RPCMixin
========

.. class:: RPCMixin

   .. method:: dispatch(request, \*args, \**kwargs)

   .. method:: execute(handler, data)

      Dispacth will pass the handler method and data to this method, which is
      expected to invoke it and return its result.

      This allows all calls to intercepted for whatever reason you feel, such
      as caching, or allowing NewRelic to report a more meaningful view name.

   .. method:: get_request_data(default=None)

      Helper method to decode the request data.

      Default implementation is identical to ``BasePublisher``, which will
      decode JSON if the content type is 'application/json' or 'text/json',
      else request.POST


.. class:: RPCView

   Simply RPCMixin already mixed with ``django.views.generic.View``


.. method:: rpc

   A decorator for RPC endpoint methods.

   Only methods decorated with this will be accessible via RPC requests.

