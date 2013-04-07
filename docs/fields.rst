
Fields
======

Fields are declared on Serialisers to pluck values from the object for deflation, as well as to cast them back when inflating.

The basic Field class can be used for any value that has a matching JSON counterpart; i.e. bools, strings, floats, dicts, lists.

There are also some for common types:
    IntegerField
    DecimalField
    DateTimeField
    DateField
    TimeField

Finally, there are the two Serialiser Fields, which will generate their value using a serialiser class.  They are the SerialiserField, and ManySerialiserField.

Field
=====

    class Field(attribute=None, default=None, readonly=False, \*args, \*\*kwargs)

    + attribute
    Used to define the attribute this field sources it value from on the object.  If omitted, the name of this field in its Serialiser class will be used.

    + default
    The value to use if we can't find a value on the object.

Deflate Cycle
=============

    Field.deflate(name, obj, data, \*\*kwargs):

    + Determine if we use name or attribute.
    + Use nap.utils.digattr to get the value
    + If the value is not None, call self.reduce
    + Add our value to the data dict under the key in name

The reduce method is the last stage of casting.  By default, it does nothing.

Inflate Cycle
=============

    Field.inflate(name, data, obj, \*\*kwargs):

    + If this field is read-only, return immediately.
    + Determine if we use name or attribute
    + Try to get our value from the data dict.  If it's not there, return.
    + Pass the value through self.restore
    + Save the value in the obj dict

By default, restore tries to construct a new self.type_class from the value, unless type_class is None.

Serialiser Fields
=================

SerialiserField follows the same pattern as above, but replaces the normal reduce/restore methods with calls to its serialisers object_deflate/object_inflate.

ManySerialiserField does the same, but uses list_deflate/list_inflate.

