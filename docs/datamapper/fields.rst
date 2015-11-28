DataMapper Fields
=================

The property built in
---------------------

DataMappers work using Python's descriptor protocol, which is most commonly
used via the `property` built-in. This gives you full control over a
DataMapper's properties. When constructing a DataMapper you can pass an
object for it to "bind" to. All field access to the DataMapper fields will
proxy to this bound object.

Here's an example to illustrate some of these concepts:

.. code-block:: python

    # An object we want to create a DataMapper for
    class Person(object):

        def __init__(self, first_name, last_name, is_alive):
            self.first_name = first_name
            self.last_name = last_name
            self.is_alive = is_alive


    from nap import datamapper

    # A DataMapper that we are creating for the Person object
    class PersonMapper(datamapper.DataMapper):

        '''
        The self argument refers to the object we bind the DataMapper to when
        we construct it. It DOES NOT refer to the instance of the PersonMapper.
        '''
        @datamapper.field
        def name(self):
            return {}.format(self.first_name, self.last_name)

        # We can use the Field class for simpler cases
        first_name = datamapper.Field('first_name')
        last_name = datamapper.Field('last_name')
        is_alive = datamapper.Field('is_alive')

    # Construct instances of the Person and a DataMapper classes
    person = Person('Jane', 'Doe', 22, True)
    mapper = DataMapper(person)

The decorator `field` works exactly like `property`, however it will operate on
the "bound" object, not the DataMapper.


Field classes
-------------
The Field classes covers simpler cases as well as allowing easier control. 
The following fields can be set on a DataMapper:


.. class:: Field(name, required=True, default=NOT_PROVIDED, filters=None)

    For simple cases 

    :param name: The name of the property on the bound object it gets/sets.
    :param default: The value to use if the source value is absent.
    :param filters: The filters to apply. Default: None
    :param required: Is this field required? Default: True

.. class:: DigField()
    
    # Todo

.. class:: MapperField(mapper)
    
    Used when serialising a model that has a foreign key relation. 

    :param mapper: A DataMapper