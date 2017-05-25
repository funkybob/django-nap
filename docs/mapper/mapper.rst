==========
Mapper API
==========

All properties and methods are prefixed with _ to avoid polluting the
namespace for your public fields.

.. class:: Mapper(obj=None, \**kwargs)

   .. attribute:: _fields

      A dict of (name: field) for all fields on this mapper.

   .. attribute:: _field_names

      A list of field names on this mapper.

   .. method:: _reduce()

      Returns a dict containing all the field values on the currently bound
      object.

   .. method:: _clean(data, full)

      Allows whole-object validation.

      Should update self._errors dict with any new validation errors.

      The `full` flag indicates if this is an _apply (True) or _patch (False)
      cycle.

   .. method:: _patch(data)

      Update all properties on this mapper supplied from the dict ``data``.

      Any omitted fields will be skipped entirely.

   .. method:: _apply(data)

      Update all properties on this mapper fron the dict ``data``.

      If a field is marked as `required` it must have either a value provided,
      or a default specified.

      All ValidationErrors raised by fields and their filters will be collected
      in a single ValidationError. You can access this dict via the exception's
      `error_dict` property.
