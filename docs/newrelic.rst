=========
New Relic
=========

If you are using NewRelic, you will want to use the hooks provided, otherwise all Nap API calls will be logged as "nap.publisher.view".

Simply add the following lines to your newrelic.ini

.. code-block:: ini

    [import-hook:nap.publisher]
    enabled = true
    execute = nap.newrelic:instrument_django_nap_publisher

