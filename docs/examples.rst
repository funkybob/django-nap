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


mappers.py
-------------

.. code-block:: python

    from nap import mapper

    class PostMapper(mapper.ModelMapper):
        class Meta:
            model = models.Post

        @mapper.field(readonly=True)
        def tags(self):
            return list(obj.tags.values_list('name', flat=True))


views.py
-------------

.. code-block:: python

    from nap.rest import views

    from . import mappers, models


    class PostMixin:
        model = models.Post
        mapper_class = mappers.PostMapper


    class PostList(PostMixin,
                   views.ListGetMixin,
                   views.BaseListMixin):
        paginate_by = 12


    class PostDetail(PostMixin,
                     views.ObjectGetMixin,
                     views.BaseObjectMixin):
        pass

urls.py
-------

.. code-block:: python

    from django.conf.urls import include, url

    from . import views

    urlpatterns = [
        (r'^api/', include([
            url(r'^post/$',
                views.PostList.as_view(),
                name='post-list'),
            url(r'^post/(?P<pk>\d+)/$',
                views.PostDetail.as_view(),
                name='post-detail'),
        ])),
    ]


Case 2: Login View
==================

Once you've defined a ``Mapper`` for your `User` model, you can provide this
Login endpoint:

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
            view = super().as_view(*args, **kwargs)
            return ensure_csrf_token(view)

        def get(self, request):
            '''Returns the current user's details'''
            if request.user.is_authenticated():
                return self.single_response(object=request.user)
            return http.Forbidden()

        def post(self, request):
            form = AuthenticationForm(request, self.get_request_data({}))
            if form.is_valid():
                auth.login(request, form.get_user())
                return self.get(request)
            return self.error_response(form.errors)


Note that it decorates `as_view` with `ensure_csrf_token`.  This ensures the
CSRF token is set if your site is a SPA.

You could even use the ``DELETE`` HTTP method for logout.

.. code-block:: python

        def delete(self, request):
            auth.logout(request)
            return self.deleted_response()

