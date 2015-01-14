============
DataView API
============

All properties and methods are prefixed with _ to avoid polluting the namespace for your public fields.

.. class:: DataView(obj=None, \**kwargs)

   .. attribute:: _fields

      A dict of (name: field) for all fields on this dataview.

   .. attribute:: _field_names

      A list of field names on this view.

   .. method:: _reduce()

      Returns a dict containing all the field values on the currently bound
      object.

   .. method:: _apply(data, full=False)

      Update all properties on this view from the dict ``data``.

      All ValidationErrors raised by fields and their filters will be collected
      in a single ValidationError. You can access this dict via the exception's
      `error_dict` property.

      If the `full` argument is True, all fields will be validated, even if no
      value is supplied for them. Otherwise they would raise ValidationErrors.
