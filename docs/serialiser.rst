===========
Serialisers
===========

Quick Overview
==============

Serialisers define how to turn a Python object into a collection of JSON compatible types.

They are defined using the familiar declarative syntax, like Models and Forms.


Serialiser objects
==================

A Serialiser class is defined much like a Form or Model:

    class MySerialiser(Serialiser):
        foo = fields.Field()
        bar = fields.Field('foo.bar')
        baz = fields.IntegerField()

Without an attribute specified, the field will use its name as the attribute name.

Serialiser methods
==================

def object_deflate(obj, \*\*kwargs):

    Returns `obj` reduced to its serialisable format.

    It calls each fields "deflate" method, passing the object, a dict for the resulting data, and kwargs.

    Then it checks if the class as a deflate_FOO method, where foo matches the field name.  If so, it sets
    the fields value in the dict to the result of calling that method, passing it the object, data dict, and kwargs.

    This allows you to customise exactly how field data are retrieved and converted.

def list_deflate(obj_list, \*\*kwargs):

    Calls object_deflate on each item in object_list.

def object_inflate(data, instance=None, \*\*kwargs):

    Turn serialisable data back into an object instance.

    First it builds a dict by performing the following steps on each declared field:
        - if it's marked readonly, it skips it
        - if there is an inflate_FOO method, it calls it, passing data, obj, instance, and kwargs
        - otherwise, it calls the fields inflate method, passing name, data, obj, and kwargs
    Once this is complete, it calls the `restore_object` method on itself, passing the data dict, instance, and kwargs.

