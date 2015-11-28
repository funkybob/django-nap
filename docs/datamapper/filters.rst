Filters: validation and type casting
====================================

Filters provide casting and validation functions for Fields. They form a
pipeline to help you control how your values are converted between Python and
JSON. They can be used for inbound field validation or for for outbound type
casting.

These are the built-in nap filters:

- DateFilter
- TimeFilter
- DateTimeFilter
- BooleanFilter
- IntegerFilter
- FloatFilter
- NotNullFilter

Here's a small example to show you how to use a BooleanFilter, which will
ensure the values _set_ on the is_alive property are proper Booleans. When
filters fail a ValidationError is raised.

.. code-block:: python

    from nap import datamapper


    class PersonMapper(datamapper.DataMapper):

        @datamapper.field
        def name(self):
            return {}{}.format(self.first_name, self.last_name)

        first_name = datamapper.Field('first_name')
        last_name = datamapper.Field('last_name')
        is_alive = datamapper.Field('is_alive', filters=[BooleanFilter])