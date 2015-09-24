from __future__ import absolute_import

from newrelic.agent import (FunctionTrace, ObjectWrapper, callable_name,
                            current_transaction, set_transaction_name)


# In agent configuration file add:
#
# [import-hook:nap.rest.publisher]
# enabled = true
# execute = nap.newrelic:instrument_django_nap_publisher



def instrument_django_nap_publisher(module):

    def execute_wrapper(wrapped, instance, args, kwargs):

        transaction = current_transaction()

        if transaction is None:
            return wrapped(*args, **kwargs)

        def _handler(handler, *args, **kwargs):
            return handler

        handler = _handler(*args, **kwargs)

        name = callable_name(handler)

        set_transaction_name(name)

        with FunctionTrace(transaction, name):
            return wrapped(*args, **kwargs)

    module.BasePublisher.execute = ObjectWrapper(
        module.BasePublisher.execute, None, execute_wrapper)
