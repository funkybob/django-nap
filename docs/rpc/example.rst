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


----------------
A Login Endpoint
----------------


.. code-block:: python

   class AuthView(rps.RPCView):

      @rpc.method
      def check(self):
          '''Check if user is logged in.'''
          return self.request.user.is_authenticated()

      @rpc.method
      def login(self, username, password):
          form = AuthenticationForm(self.request, {
              'username': username,
              'password': password,
          })
          if form.is_valid():
              auth.login(self.request, form.get_user())
              return True
          return False

      @rpc.method
      def logout(self):
          if self.request.user.is_authenticated():
              auth.logout(self.request)
              return True
          return False
