=============
Authorisation
=============

Authorisation is handled using the ``permit`` decorator factory.

Use it to decorate any handler method, passing it a function that will yield
True/False.  If the function returns False, a `http.Forbidden` response is
returned. Otherwise, the handler is invoked.

The function will be passed all the arguments the handler will receive.

Pre-defined
===========

For convenience some decorators are already defined:

.. function:: nap.auth.permit_logged_in

   Tests if request.user.is_authenticated() is true.

.. function:: nap.auth.permit_staff

   Tests if request.user.is_staff is true.

Example:

Requiring logged in users for a specific handler.

.. code-block:: python

   from nap.auth import permit_logged_in
   from nap import rest

   class WidgetPublisher(rest.Publisher):

       @permit_logged_in
       def list_get_default(self, request):
       ...

Mixins
======

Also provided are two mixin classes for affecting permission checks across all
requests.

They work equally well for Publisher and Class-Based Views.

.. class:: nap.rest.auth.LoginRequiredMixin

   Wraps the ``dispatch`` method with the `permit_logged_in` decorator.

.. class:: nap.rest.auth.StaffRequiredMixin

    Wraps the ``dispatch`` method with the `permit_staff` decorator.
