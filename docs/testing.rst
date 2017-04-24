=======
Testing
=======


To help with writing tests, there are some utilities provided.

``nap.utils.test.JsonClient``

A subclass of django.test.Client that additionally supports a ``json``
argument. When provided, the content type of the request will be `text/json`,
and the ``json`` argument will be JSON encoded and passed as the ``data``.


``nap.utils.test.ApiTestCase``


Subclasses django.test.TestCase to provide additional helpers.

   .. method:: assertResponseCode(url, status_code, method='get', \**kwargs):

      Assert that making the request yields the expected status code.
      Returns the request result.
