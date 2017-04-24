========
Examples
========

Sometimes, an example is much easier to understand than abstract API docs, so here's some sample use cases.

Case 1: Simple Blog API
=======================

models.py
---------

.. code-block:: python

    from django.db import models
    from taggit.managers import TaggableManager

    class Post(models.Model):
        title = models.CharField(max_length=255)
        author = models.ForeignKey('auth.User')
        published = models.BooleanField(default=False)
        content = models.TextField(blank=True)
        tags = TaggableManager(blank=True)


serialiser.py
-------------

.. code-block:: python

    from nap import serialiser
    from nap.serialiser import fields

    class PostSerialiser(serialiser.ModelSerialiser):
        class Meta:
            model = models.Post

        tags = fields.Field()

        def deflate_tags(self, obj, \**kwargs):
            '''Turn the tags into a flat list of names'''
            return [tag.name for tag in obj.tags.all()]


publishers.py
-------------

.. code-block:: python

    from nap import rest
    from .serialiser import PostSerialiser

    class PostPublisher(rest.ModelPublisher):
        serialiser = PostSerialiser()

urls.py
-------

.. code-block:: python

    from .publishers import PostPublisher

    urlpatterns = [
        (r'^api/', include(PostPublisher.patterns())),
    ]


Case 2: Login View
==================

Once you've defined a ``DataMapper`` for your `User` model, you can provide
this simple Login endpoint:

.. code-block:: python

    from django.contrib import auth
    from django.contrib.auth.forms import AuthenticationForm
    from django.utils.decorators import classonlymethod
    from django.views.decorators.csrf import ensure_csrf_cookie

    from nap.rest import views

    from . import mappers

    class LoginView(views.BaseObjectView):
        mapper_class = mappers.UserMapper

        @classonlymethod
        def as_view(cls, *args, **kwargs):
            view = super(LoginView, cls).as_view(*args, **kwargs)
            return ensure_csrf_token(view)

        def get(self, request):
            '''Returns the current user's details'''
            if request.user.is_authenticated():
                return self.single_response(object=request.user)
            return http.Forbidden()

        def post(self, request):
            if request.user.is_authenticated():
                auth.logout(request)
            form = AuthenticationForm(request, self.get_request_data({}))
            if form.is_valid():
                auth.login(request, form.get_user())
                return self.get(request)
            return self.error_response(form.errors)


Note that it decorates `as_view` with `ensure_csrf_token`.  This ensures the
CSRF token is set if your site is a SPA.
