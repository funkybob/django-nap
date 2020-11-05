=========
Changelog
=========

-------
Current
-------

v0.40.0 (2018-??-??)
====================

.. admonition:: Python and Django version support change

   As of this release, Django 2.0+ is required.

   As a result, Python 3.4+ is also required.

Incompatible Changes:

- ``nap.rest.views.BaseListView`` and ``name.rest.views.BaseObjectView`` have
  been renamed to ``nap.rest.views.ListBaseView`` and
  ``nap.rest.views.ObjectBaseView`` respectively.
- ``nap.views.rest.MapperMixin.error_response`` now calls ``get_json_data`` on
  the ``errors`` parameter.

Enhancements:

- Mappers now use ``django.forms.utils.ErrorDict`` and
  ``django.forms.utils.ErrorList`` for errors.
- ``nap.utils.JsonMixin.get_request_data`` now uses ``cgi.FieldStorage`` to
  parse request data, allowing it to support files in multi-part bodies for PUT
  and PATCH requests.
- ``nap.mapper.fields.field`` will now default to `readonly` = `True` unless a
  setter is specified.

Removed:

- ``nap.utils.flatten_errors`` has been removed.

Bug Fixes:

- Make `except_response` use `functools.update_wrapper` to not disguise the
  view function.

-------
History
-------

v0.30.11 (2017-03-31)
=====================

Enhancements:

- Simplify ``nam.mapper.base.MetaMapper`` discovering fields.
- Simplify ``nap.mapper.models.MetaMapper`` accordingly.

Bug Fixes:

- Added a dummy `post` method to ``nap.rpc.views.RpcMixin`` so ``View``
  believes `POST` is an acceptable method.
- Fix fallback when looking for object/object_list/mapper in REST views.

v0.30.10 (2017-08-24)
=====================

Enhancements:

- JsonMixin will use request.content_type and request.content_params in Django
  1.10+, instead of parsing them itself.
- NapView now decorates the as_view response with except_response, instead of
  overriding dispatch.
- Simplified code that builds ModelMapper
- RPCView now uses NapView to handle exception responses.
- Micro-optimsations for ``nap.extras.simplecsv.Writer``

Bug Fixes:

- A ``TypeError`` or ``ValueError`` raised in ``nap.mapper.Field.set`` will now
  be caught and raised as a ``ValidationError``.

v0.30.9 (2017-06-26)
====================

Enhancements:

- Add `MapperMixin.include_meta` as an override to including meta in responses.
- Moved `StreamingJSONResponse` into `nap.http.response`
- Moved `except_response` into `nap.http.decorators`

v0.30.8 (2017-06-09)
====================

Enhancements:

- `MapperMixin.get_meta(page)` was added to allow customising of meta-data in
  response.

Deprecations:

- `MapperMixin` no longer provides default values of None for `mapper`,
  `object` and `object_list`.

v0.30.7 (2017-06-07)
====================

.. admonition:: The prototype for `context_field` has been changed.

   See documentation for details.

Enhancements:

- Allow `ModelMapper` to inherit its `Meta` from a parent.
- Add ``nap.http.StreamingJSONResponse``.
- Add tools to help support generators in JSON encoding
- Changed `context_field` to pass the Mapper._context as the last argument to
  the getter and setter methods.

v0.30.6 (2017-05-29)
====================

Enhancements:

- Added custom __set__ method for `ToManyField` so it can call `set` on the
  manager.

Bug Fixes:

- Don't replace inherited fields with auto-added model fields.
- Return a list of PKs if no Mapper provided to ToManyField

v0.30.5 (2017-05-27)
====================

Enhancements:

- Added pagination support to `MapperMixin.multiple_response`
- Import all fields into mapper namespace
- Allow passing \**kwargs to all CBV `valid_FOO` methods.

Bug Fixes:

- Call `all()` on `Manager` instances in `ToManyfield`

Deprecations:

- Removed `newrelic` module, as it was only to support Publishers.

v0.30.4 (2017-05-25)
====================

Enhancements:

- Added `nap.utils.NapJSONEncoder` to support `__json__` protocol.

Bug Fixes:

- Fixed __new__ on field so subclasses work.
- Reworked context_field to work properly, and match docs.

v0.30.3 (2017-05-24)
====================

Enhancements:

Bug Fixes:

- Using @foo.setter on a field will now retain other keyword arguments.
- RPCClient now sets Content-Type on request.

v0.30.2 (2017-05-23)
====================

Enhancements:

- Began documenting the `extras` module.

Bug Fixes:

- Fixed ToOneField to reference `self.related_model` not `self.model`

v0.30.1 (2017-05-18)
====================

Enhancements:

- fields will now raise and error when trying to set a value with no setter.

Bug Fixes:

- Include null in field constructor
- Set null correctly in fields on ModelMapper
- Handle null ForeignKey/OneToOneFields properly

Deprecations:

- Dropped `nap.utils.digattr` and `nap.mapper.fields.DigField`
- Typed fields no longer special case None

v0.30.0 (2017-05-16)
====================

.. admonition:: Python and Django version support change

   Support for Python2 has been dropped.

   Support for Django 1.7 is no longer tested.

.. warning:: API Breakage

   Another large code reorganisation was undertaken.
   `DataMapper` has been renamed to `Mapper`, and large amounts of its cod
   have been rewritten.

   Filters are no longer supported.

Enhancements:

- Added `readonly` attribute to `Mapper.field`
- Added `readonly` list to `ModelMapper.Meta`
- All `MapperMixin.*_response` methods now accept kwargs, and try to
  `setdefault` their default behaviour in it.
- In PUT/POST REST views, the `*_valid` methods now accept kwargs and pass them
  to their response class.
- Added RPC Client example code.
- Dropped deprecated test class.

Bug Fixes:

- Corrected `Mapper` to work as documented for ``obj = data << dm``

v0.20.3 (2017-05-09)
====================

Bug Fixes:

- Handle None values properly in ModelFilter

v0.20.2 (2017-05-06)
====================

Enhancements:

- Added `nap.http.except_response` decorator to handle exceptional responses in
  view functions.
- Finished updating `nap.extras.actions.ExportCsv` to work with DataMappers.

v0.20.1 (2017-05-04) ... be with you!
=====================================

Bug Fixes:

- Remove `default_app_config` [Thanks nkuttler]

v0.20.0 (2017-04-24)
====================

.. admonition:: WARNING: Major Refactor

   All code related to Publishers and Serialisers have been removed.

   Many

Enhancements:

- Add a common base class `HttpResponseError` for Status 4xx and 5xx responses.
- JsonMixin imports settings late to avoid problems

Deprecation:

- Removed backward compatibility shim for JsonResponse, now that we require
  Django 1.7
- Removed Publishers
- Removed Serialisers
- Removed auth - use Django's built in mixins.
- Removed SerialisedResponseMixin

v0.14.9 (2015-12-08)
====================

Enhancements:

- Dropped support for testing in older Django
- Add ModelFilter to ForeignKeys in ModelDataMapper
- Allow passing kwargs to `JsonMixin.loads` and `JsonMixin.dumps`
- Added ability to change the response class used in auth decorators.
- Added `>>=` to `ModelDataMapper` to allow applying to new model instance.

Bug Fixes:

- Add any fields not in a supplied `Meta.fields` for a `ModelDataMapper` to the
  excludes list to ensure model validation also excludes them.
- Fixed `utils.JsonClient` to actually work.
- Propery handle encoding in `JsonMixin.get_request_data` for PUT and PATCH.


v0.14.8 (2015-10-12)
====================

Enhancements:

- Added `Ripper` class to utils.
- Use `six.moves.urllib` instead of our own try/except on import
- Micro-optimisation: Calculate fields and field names for DataMappers at
  declatation
- Added `NapView` to `nap.rest.views` to handle when custom `http` responses
  are raised.
- Change default DELETE response to be empty
- Added `nap.rest.views.NapView` to catch and return
  `nap.http.BaseHttpResponse` exceptions as responses.

Bug Fixes:

- Set safe=False in MapperMixin.empty_response

v0.14.7.1 (2015-09-29)
======================

Enhancements:

- Simplified `auth.permit_groups`

Bug Fixes:

- On a DataMapper, if a Field's default is callable, call it.
- Make _CastFiler and Date/Time filters skip to_python if value is of right
  type already.

v0.14.7 (2015-09-29)
====================

Enhancements:

+ Allow passing extra arguments to MapperMinix.ok_response
+ Add `required` and `default` options for datamapper.field
+ Add `LoginRequiredMixin` and `StaffRequiredMixin` to `nap.rest.auth`
+ Allow use of custom JSONEncoder/JSONDecoder with JsonMixin

v0.14.6 (2015-09-14)
====================

Enhancements:

+ Make MapperMixin.single_response and MapperMixin.multiple_response get
  mapper, object, and queryset if none is provided.
+ Dropped testing support for older versions of Django
+ Added DataMapper tutorial to docs (Thanks limbera!)
+ Added ModelFilter to DataMapper
+ Reworked Publisher URLs to be easier to customise, and more consistent
+ Added test module
+ ModelDataMapper now creates a new Model instance if not passed one at
  construction.
+ Pass list of excluded fields to Model.full_clean()

v0.14.5.1 (2015-08-06)
======================

Bug Fixes:

- Use six.string_types not str in flatten_errors
- Properly update error dict in ModelDataMapper._clean

v0.14.5 (2015-08-06)
====================

Enhancements:

- Add _clean method to DataMapper for whole-object cleaning.
- Make ModelDataMapper._clean call instance.full_clean.

Bug Fixes:

- Fix ModelDataMapper to not get confused by ``six.with_metaclass`` hacks.
- Fix ListMixin.ok_response to call self.multiple_response not
  self.list_response

v0.14.4 (2015-05-19)
====================

Enhancements:

- Fix travis config
- Simplify AppConfig usage
- Switched from using Django's HTTP reason phrases to Python's.
- Tidied the abstractions of response helpers in django.rest.views.
- Added BaseListView and BaseObjectView to django.rest.views.

Bug Fixes:

- Use our own get_object_or_404 shortcut in ModelPublisher.
- Fixed rest.views to closer match RFC [Thanks Ian Wilson]

v0.14.3 (2015-02-17)
====================

Ehancements

+ JsonMixin.get_request_data will now handle form encoded data for PUT
+ Change API for datamapper to separate _apply and _patch.

v0.14.2 (2015-01-23)
====================

.. admonition:: WARNING: Removed module

   The module nap.exceptions has been completely removed.

Enhancements:

+ Switched custom ValidationError / ValidationErrors to django's
  ValidationError
+ Added DataMapper library
+ Added CBV mixins for composing API Views that use DataMappers


v0.14.1.1
=========

Bug Fixes:

+ Add required `name` attribute to AppConfig [thanks bobobo1618]

v0.14.1
=======

Enhancements:

+ Import REASON_CODES from Django
+ Use Django's JsonResponse if available, or our own copy of it.
+ Unify all json handling functions into utils.JsonMixin
+ Add RPCView introspection
+ Use Django's vendored copy of 'six'
+ Add new runtests script

Bug Fixes:

+ Cope with blank content encoding values in RPC Views
+ Raise a 404 on invalid page_size value
+ Validate the data we got in RPC View is passable as \**kwargs
+ ISO_8859_1 isn't defined in older Django versions
+ Emulate django template lookups in digattr by ignoring callables flagged
  'do_not_call_in_templates'

v0.14.0
=======

.. admonition:: WARNING: API breakage

   A large reorganisation of the code was undertaken.

   Now there are 3 major top-level modules:
   - serialiser
   - rest
   - rpc

Enhancements:

+ Added functional RPC system [merged from django-marionette]
+ Made most things accessible in top-level module

v0.13.9
=======

Enhancements:

+ Added Django 1.7 AppConfig, which will auto-discover on ready
+ Added a default implementation of ModelPublsiher.list_post_default
+ Tidied code with flake8

Bug Fixes:

+ Fixed use of wrong argument in auth.permit_groups

v0.13.8
=======

Enhancements:

+ Added prefetch_related and select_related support to ExportCsv action
+ Added Field.virtual to smooth changes to Field now raising AttributeError,
  and support optional fields

v0.13.7
=======

Enhancements:

+ Added ReadTheDocs, and prettied up the docs
+ Use Pythons content-type parsing
+ Added RPC publisher [WIP]
+ Allow api.register to be used as a decorator
+ Make Meta classes more proscriptive
+ Allow ModelSerialiser to override Field type used for fields.
+ Added ModelReadSerialiser and ModelCreateUpdateSerialiser to support more
  complex inflate scenarios [WIP]

Bug Fixes:

- Fixed ExportCsv and simplecsv extras
- Raise AttributeError if a deflating a field with no default set would result
  in using its default. [Fixes #28]
- Fixed auto-generated api_names.
- Purged under-developed ModelFormMixin class

v0.13.6
=======

Enhancements:

+ Overhauled testing
+ Added 'total_pages' to page meta.
+ Added Serialiser.obj_class

v0.13.5.1
=========

Bug Fixes:

- Fix fix for b'' from last release, to work in py2

v0.13.5
=======

Bug Fixes:

- Fix use of b'' for Py3.3 [thanks zzing]

Enhancements:

+ Add options to control patterns

v0.13.4
=======

Bug Fixes:

- Return http.NotFound instead of raising it

Enhancements:

+ Added views publisher
+ Updated docs
+ Re-added support for ujson, if installed
+ Tidied up with pyflakes/pylint
+ Added Publisher.response_class property

v0.13.3
=======

Bugs Fixed:

- Make API return NotFound, instead of Raising it
- Remove bogus CSV Reader class

v0.13.2.1
=========

Bugs Fixed:

- Fixed typo
- Fixed resolving cache in mixin

v0.13.2
=======

Enhancements:

+ Separate Publisher.build_view from Publisher.patterns to ease providing
  custom patterns
+ Added SimplePatternsMixin for Publisher
+ Added Publisher.sort_object_list and Publisher.filter_object_list hooks

v0.13.1
=======

Bugs Fixed:

- Fixed silly bug in inflate

v0.13.0
=======

.. admonition:: WARNING: API breakage

   Changed auto-discover to look for 'publishers' instead of 'seraliser'.

Enhancements:

+ Added Field.null support
+ Now use the Field.default value
+ ValidationError handled in all field and custom inflator methods

v0.12.5.1
=========

Bugs Fixed:

- Fix mistake introduced in 0.12.3 which broke NewRelic support

v0.12.5
=======

Bugs Fixed:

- Restored Django 1.4 compatibility

Enhancements:

+ Allow disabling of API introspection index

v0.12.4
=======

Bugs Fixed:

- Fixed filename generation in csv export action
- Fixed unicode/str issues with type() calls

Enhancements:

+ Split simplecsv and csv export into extras module
+ Merged engine class directly into Publisher
+ Added fields.StringField

v0.12.3
=======

Bugs Fixed:

- Fix argument handling in Model*SerialiserFields
- Tidied up with pyflakes

Enhancements:

+ Added support for Py3.3 [thanks ioneyed]
+ Overhauled the MetaSerialiser class
+ Overhauled "sandbox" app
+ Added csv export action

v0.12.2
=======

Enhancements:

+ Support read_only in modelserialiser_factory

v0.12.1
=======

Bugs Fixed:

- Flatten url patterns so object_default can match without trailing /
- Fix class returned in permit decorator [Thanks emilkjer]

Enhancements:

+ Allow passing an alternative default instead of None for
  Publisher.get_request_data
+ Added "read_only_fields" to ModelSerialiser [thanks jayant]

v0.12
=====

Enhancements:

+ Tune Serialisers to pre-build their deflater/inflater method lists, removing
  work from the inner loop
+ Remove \*args where it's no helpful

v0.11.6.1
=========

Bugs Fixed:

- Renamed HttpResponseRedirect to HttpResponseRedirection to avoid clashing
  with Django http class

v0.11.6
=======

Bugs Fixed:

- Raise a 404 on paginator raising EmptyPage, instead of failing

v0.11.5.1
=========

Bugs Fixed:

- Fix arguments passed to execute method

v0.11.5
=======

Enhancements:

+ Add Publisher.execute to make wrapping handler calls easier [also, makes
  NewRelic simpler to hook in]
+ Allow empty first pages in pagination
+ Added support module for NewRelic

v0.11.4
=======

Enhancements:

+ Make content-type detection more forgiving

v0.11.3
=======

Enhancements:

+ Make get_page honor limit parameter, but bound it to max_page_size, which
  defaults to page_size
+ Allow changing the GET param names for page, offset and limit
+ Allow passing page+limit or offset+limit

v0.11.2
=======

Enhancements:

+ Added BooleanField
+ Extended tests
+ Force CSRF protection

v0.11.1
=======

Enhancements:

+ Changed SerialiserField/ManySerialiserField to replace reduce/restore instead
  of overriding inflate/deflate methods
+ Fixed broken url pattern for object action
+ Updated fields documentation

v0.11
=====

.. admonition:: API breakage

    Serialiser.deflate_object and Serialiser.deflate_list have been renamed.

Enhancements:

+ Changed deflate_object and deflate_list to object_deflate and list_deflate to
  avoid potential field deflater name conflict
+ Moved all model related code to models.py
+ Added modelserialiser_factory
+ Updated ModelSerialiserField/ModelManySerialiserField to optionally
  auto-create a serialiser for the supplied model

v0.10.3
=======

Enhancements:

+ Added python2.6 support back [thanks nkuttler]
+ Added more documentation
+ Added Publisher.get_serialiser_kwargs hook
+ Publisher.get_data was renamed to Publisher.get_request_data for clarity

v0.10.2
=======

Bugs Fixed:

- Removed leftover debug print

v0.10.1
=======

Enhancements:

+ Added Publisher introspection
+ Added LocationHeaderMixin to HTTP classes

v0.10
=====

Bugs Fixed:

- Removed useless cruft form utils

Enhancements:

+ Replaced http subclasses with Exceptional ones
+ Wrap call to handlers to catch Exceptional http responses

v0.9.1
======

Enhancements:

+ Started documentation
+ Added permit_groups decorator
+ Minor speedup in MetaSerialiser

v0.9
====

Bugs Fixed:

- Fixed var name bug in ModelSerialiser.restore_object
- Removed old 'may' auth API

Enhancements:

+ Added permit decorators
+ use string formatting not join - it's slightly faster

v0.8
====

Enhancements:

+ Added create/delete methods to ModelPublisher
+ Renamed HttpResponse subclasses
+ Split out BasePublisher class
+ Added http.STATUS dict/list utility class

.. note::

   Because this uses OrderedDict nap is no longer python2.6 compatible


v0.7.1
======

Enhancements:

+ Use first engine.CONTENT_TYPES as default content type for responses

v0.7
====

Bugs Fixed:

- Removed custom JSON class

Enhancements:

+ Added Engine mixin classes
+ Added MsgPack support
+ Added type-casting fields

v0.6
====

Bugs Fixed:

- Fixed JSON serialising of date/datetime objects

Enhancements:

+ Added index view to API
+ Make render_single_object use create_response
+ Allow create_response to use a supplied response class

v0.5
====

Enhancements:

+ Added names to URL patterns
+ Added "argument" URL patterns

v0.4
====

Enhancements:

+ Added next/prev flags to list meta-data
+ Added tests

v0.3
====

Enhancements:

+ Changed to more generic extra arguments in Serialiser

v0.2
====

Bugs Fixed:

- Fixed bug in serialiser meta-class that broke inheritance
- Fixed variable names

Enhancements:

+ Pass the Publisher down into the Serialiser for more flexibility
+ Allow object IDs to be slugs
+ Handle case of empty request body with JSON content type
+ Added SerialiserField and ManySerialiserField
+ Added Api machinery
+ Changed Serialiser to use internal Meta class
+ Added ModelSerialiser class

v0.1
====

Enhancements:

+ Initial release, fraught with bugs :)
