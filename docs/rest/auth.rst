=============
Authorisation
=============

Authorisation is handled using the ``permit`` decorator.

Use it to decorate any handler method, passing it a function that will yield True/False.

The function will be passed all the arguments the handler will receive.
