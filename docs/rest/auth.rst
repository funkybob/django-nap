=============
Authorisation
=============

Nap provides two mixin classes to help affect authorisation control.

.. class:: nap.rest.auth.LoginRequiredMixin

   Wraps the ``dispatch`` method with the `permit_logged_in` decorator.

.. class:: nap.rest.auth.StaffRequiredMixin

   Wraps the ``dispatch`` method with the `permit_staff` decorator.


Additionally, there is a generic class to help you apply your own
authorisation:

.. class:: nap.rest.auth.AuthorisationMixin

   .. attribute:: permit

      A decorator that will be applied to  the view function returned by
      ``as_view``.
