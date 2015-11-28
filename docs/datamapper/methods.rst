DataMapper Methods
====================

A DataMapper supports several methods:

``_reduce()`` will reduce the instance to its serialisable state, returning a
dict representation of the DataMapper.

``_patch(data)`` will partially update (patch) a DataMapper's fields with the
values you pass in the data dict. If validation fails it will raise a
ValidationError.

``_apply(data)`` will fully update (put) a DataMapper's fields with the
values you pass in the data dict. If you don't pass a field in the data dict
it will try to set the field to the default value. If there is no default and
the field is required it will raise a ValidationError.

``_clean(data, full=True)`` is a hook for final pass validation. It allows you
to define your own custom cleaning code. You should update the ``self._errors``
dict. The ``full`` boolean indicates if the calling method was ``_apply``
(True) or ``_patch`` (False).

Here is some code to explain how these concepts work. We will continue to use
the Person class and PersonMapper class defined above. 

Note that you will need to save the result of the _apply or _patch methods if
you want to save a model to the database. 

_reduce:
---------------

.. code-block:: python

    p = Person('Jane', 'Doe', True)
    m = PersonMapper(p)
    reduced_p = m._reduce()
    print(reduced_p)

    # Output: {'first_name': 'Jane', 'last_name': 'Doe', 'is_alive': True}


_apply:
---------------

.. code-block:: python

    m = PersonMapper()
    m._apply({
        "first_name": "Jane",
        "last_name": "Doe",
        "is_alive": False
    })
    reduced = m.reduce()
    print(reduced)

    # Output: {'first_name': 'Jane', 'last_name': 'Doe', 'is_alive': False}


_patch:
---------------

.. code-block:: python

    p = Person('Jane', 'Doe', True)
    m = PersonMapper(p)
    m._patch({"last_name": "Notdoe"}) # This should patch last_name
    reduced = m.reduce()
    print(reduced)

    # Output: {'first_name': 'Jane', 'last_name': 'Notdoe', 'is_alive': True}

_clean:
---------------

.. code-block:: python

    # Todo