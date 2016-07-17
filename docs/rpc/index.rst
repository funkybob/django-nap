===
RPC
===

The RPC View allows your application to provide APIs that don't mate up with
REST patterns.

How does it work?
=================

Any POST request with a ``X-RPC-Action`` header will be intercepted and treated
as a RPC request.  If there is a method on the view class which matches the name
in the header, and it's been decorated as ``@method`` accessible, the request
data will be parsed, passed as keyword arguments to the method, and the result
JSON encoded and returned.

.. toctree::

   example
