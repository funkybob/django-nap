===================
DataMapper Tutorial
===================

In this tutorial we will write a small django-nap powered RESTful service for a
to-do list application. The tutorial has been tested against Django (1.8.3) and
django-nap (0.14.5.1).

Instead of using a more 'traditional' `Serialiser` based approach to building
the service, we will use nap's powerful `Datamappers` and Django CBV mixins.

1. Setup
========

First things first, as with any Python programming application, we want to
create a virtual environment sandbox for us to manage our applications
dependencies. Let's get started by creating a virtual environment and
activating it:

.. code-block:: python

    virtualenv nap-todo
    source nap-todo/bin/activate

If you see `(nap-todo)` prefixed to all of your terminal commands you'll know
that you correctly created and activated the virtual environment.

Next we're going to need to install Django and django-nap in our virtual
environment. Go ahead and execute the following commands to do that:

.. code-block:: python

    pip install django
    pip install django-nap

Great! We've now installed Django and django-nap and are ready to start
building our API service. Let's create a new Django project.

.. code-block:: python

    django-admin.py startproject todoproject

Change directory into the newly created todoproject directory. We'll now create
a new Django app inside the todoproject.

.. code-block:: python

    cd todoproject
    python manage.py startapp todoapp

That's great, our project directory is all set up and ready for us to start
creating the models that we will use in our application.


2. Models
==============

Our application is going to allow a `User` to create `Lists` of `Items`.
`Items` represent task that are to be done. A `List` represents collections of
`Items`. Each `Item` is associated with a `User` (from
``django.contrib.auth``). Let's begin by adding the models we want to the
todoapp/models.py file.

.. code-block:: python

    class List(models.Model):
        name = models.CharField(max_length=64)

        def __str__(self):
            return self.name


    class Item(models.Model):
        title = models.CharField(max_length=64)
        list = models.ForeignKey('todoapp.List')
        completed = models.BooleanField(default=False)
        owner = models.ForeignKey('auth.User')

        def __str__(self):
            return self.title

Next we need to create a migration and migrate the database. In your terminal
window execute the following commands:

.. code-block:: python

    python manage.py makemigration
    python manage.py migrate

Awesome let's move on to the next step.


3. DataMappers
===================

We need DataMappers to reduce Python objects into simple data types supported
by JSON and back again. nap's `DataMappers` are an alternative approach to
traditional `Serialisers`. They serve the same function, but do it in slightly
different ways. A `DataMapper` will map properties on itself to your object.
This allows you to easily convert from JSON to Python objects and vice-versa.

DataMapper for User
-------------------

Let's start by creating a `DataMapper` for the `User` model so that you can get
a better feel for how it works. A `ModelDataMapper` is a shortcut that creates
a `DataMapper` and automatically generates a set of fields for you based on the
model. Similarly to how `ModelForms` and `Forms` relate.

Let's create a new file in the todoapp directory called mappers.py and add the
following code to your todoapp/mappers.py file:

.. code-block:: python

    from django.contrib.auth.models import User

    from nap import datamapper


    class UserMapper(datamapper.ModelDataMapper):
        class Meta:
            model = User
            fields = '__all__'

The `ModelDataMapper` will create a DataMapper for us and all we need to tell
it is which model we want to map, and which fields to use. As you can see we
have told the `ModelDataMapper` to use __all__ of the User fields.

DataMapper for List
-------------------

Next let's add a `ModelDataMapper` for the `List` model. This should be very
similar to the `ModelDataMapper` we created for the User model. Your
todoapp/mappers.py file should now look like this:

.. code-block:: python

    from django.contrib.auth.models import User

    from nap import datamapper

    from . import models # Don't forget this


    class UserMapper(datamapper.ModelDataMapper):
        class Meta:
            model = User
            fields = '__all__'


    class ListMapper(datamapper.ModelDataMapper):
        class Meta:
            model = models.List
            fields = '__all__'

DataMapper for Item
-------------------

Next let's add a `ModelDataMapper` for the Item model. This ones a little
different though because there are some more complicated fields in the `Item`
model than there are in our `User` and `List` models. Let's start by
implementing the parts of the `ItemMapper` we know. We're going to add a
`ModelDataMapper` for `Item` to our code in the todoapp/mappers.py file so that
it looks like this:

.. code-block:: python

    from django.contrib.auth.models import User

    from nap import datamapper

    from . import models


    class UserMapper(datamapper.ModelDataMapper):
        class Meta:
            model = User
            fields = '__all__'


    class ListMapper(datamapper.ModelDataMapper):
        class Meta:
            model = models.List
            fields = '__all__'


    class ItemMapper(datamapper.ModelDataMapper):
        class Meta:
            model = models.Item
            fields = '__all__'
            exclude = ['owner', 'list']

As you can see we've defined the model and fields we want, but this time we're
also telling the `ModelDataMapper` which fields to exclude. We're going to
exclude the more complicated Foreign Key fields, owner and list, and deal with
them later.

Now that we've got our `DataMappers` implemented for all of our models, we can
go on to create the URLs and views for our RESTful service.


4. Class-Based Views and URLs
=============================

Let's being by add a pattern for /api/ to our root url configuration
(todoproject/urls.py). Your root url configuration should look something like
this now:

.. code-block:: python

    from django.conf.urls import include, url
    from django.contrib import admin


    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^api/', include('todoapp.urls')),
    ]

You'll notice that we've used ``include`` to point all requests to /api/ on to
``'todoapp.urls'`` but if you've been following closely you'll realise we don't
actually have a module called todoapp.urls! Let's fix that up quickly... create
a urls.py file in the todoapp directory. Now we can edit the todoapp/urls.py
file and start to think about what endpoints we want to create. I like to write
mine in the urls.py file as comments, and uncomment them as I write the view
code.

List of endpoints in words
--------------------------

1. Get a list of all of the ``List`` resources
2. Add a new List resource to the list of ``List`` resources
3. Get a single instance of a ``List`` resource
4. Get a list of all of the ``Item`` resources
5. Add a new Item resource to the list of ``Item`` resources
6. Get a single instance of an ``Item`` resource
7. Authenticate a users username and password combination

Let's add some endpoints (as comments) to the todoapp/urls.py file that will
achieve this. I've added a comment next to each endpoint that explains which of
the "List of endpoints in words" section the url will handle.

.. code-block:: python

    from django.conf.urls import include, url

    from . import views
    from . import rest_views


    urlpatterns = [
        # /api/list/ # GET will deal with (1) and POST will deal with (2)
        # /api/list/<id>/ # GET will deal with (3)
        # /api/item/ # GET will deal with (4) and POST will deal with (5)
        # /api/item/<id>/ # GET will deal with (6)
        # /api/login/ # POST will deal with 7
    ]

Writing the view: list of List
-------------------------------

Now that we know what endpoints we are planning to build, and what each will
need to do we can create the views that will process the requests. Let's create
a new file called rest_views.py in the todoapp directory. We're going to start
by implementing (1) which requires us to: "get a list of all of the ``List``
resources"

Lets add the following code to the todoapp/rest_views.py file:

.. code-block:: python

    from nap.rest import views

    from . import mappers
    from . import models


    class ListListView(views.BaseListView):
        model = models.List
        mapper_class = mappers.ListMapper

Given we want to get a list of all the List resources, we will use the
``nap.rest.views.BaseListView`` as a starting point. The BaseListView combines
ListMixin (which extends Django's MultipleObjectMixin) with View. From the
Django docs: "MultipleObjectMixin can be used to display a list of objects."
This sounds like what we need!

Adding GET functionality: list of List
--------------------------------------

We do however want to use ``nap.rest.views.ListGetMixin`` which provides the
get() method for lists. This means the HTTP verb GET can now be used with our
view. We need to update our ``ListListView(views.BaseListView)`` class to
include the ``ListGetMixin`` so lets do that.

Update your todoapp/rest_views.py file to look like this:

.. code-block:: python

    from nap.rest import views

    from . import mappers
    from . import models


    class ListListView(views.ListGetMixin, views.BaseListView):
        model = models.List
        mapper_class = mappers.ListMapper

Adding POST functionality: list of List
---------------------------------------

We decided when planning our URLs, that to add a List resource to the list of
Lists, we'd POST to the same url (/api/list/). That's as simple as including
the ``ListPostMixin`` to the ``ListListView``. This will provide the post()
method which will allow us to use the POST HTTP verb.

Let's go ahead and do that now. Update your todoapp/rest_views.py file to look
like this:

.. code-block:: python

    from nap.rest import views

    from . import mappers
    from . import models


    class ListListView(views.ListPostMixin, views.ListGetMixin, views.BaseListView):
        model = models.List
        mapper_class = mappers.ListMapper

Defining the URL: list of List
------------------------------

One last thing before we take our API for a test drive. We need to uncomment
the api endpoint for /api/list/ and actually write the proper URL pattern.
We're going to cheat a little here and use the inbuilt Django ``@csrf_exempt``
decorator to bypass CSRF, but please ALWAYS use CSRF in production code.

Update your todoapp/urls.py to look like this:

.. code-block:: python

    from django.conf.urls import include, url
    from django.views.decorators.csrf import csrf_exempt

    from . import views
    from . import rest_views


    urlpatterns = [
        url(r'^list/$', csrf_exempt(rest_views.ListListView.as_view())),
        # /api/list/<id>/ # GET will deal with (3)
        # /api/item/ # GET will deal with (4) and POST will deal with (5)
        # /api/item/<id>/ # GET will deal with (6)
        # /api/login/ # POST will deal with 7
    ]

You can see that we've mapped the list/ endpoint to ListListView class that we
wrote earlier. Now that we have built the functionality to create Lists and
view Lists it's time to see if our API works.

Testing with Python Requests: list of List
------------------------------------------

We'll use Python Requests (http://www.python-requests.org/) to POST a List
object to our database. In a terminal window that you have activated your
virtual environment in, run your HTTP server with
``python manage.py runserver``. Open up a second terminal window, active your
virtual environment as before. Install Requests with ``pip install requests``.
Open the Python interpreter by typing ``python`` at the console. This is not a
tutorial on using requests so just enter this boilerplate code into your Python
interpreter:

.. code-block:: python

    import requests
    payload = {'name': 'my demo list'}
    r = requests.post("http://127.0.0.1:8000/api/list/", params=payload)
    r.status_code

The result of r.status_code should be ``HTTP 201 Created``. This will confirm
that we've created a list in our database with the name 'my demo list'. You can
confirm this by looking at the admin interface at http://127.0.0.1:8000/admin.
Remember you may need to create a superuser in order to use the admin interface.

So now that we've got a List instance in our database, we can execute a GET to
the /api/list/ endpoint and we should receive a JSON response. We don't need to
use Requests for this because our browser provides all the GET functionality
that we need. Simply load the url http://127.0.0.1:8000/api/list/ in your
browser and you should see a JSON representation of all of the lists (at this
stage only 1) in your database. You should play around with Requests and add
some more List instances to the database.

Recap: list of List
-------------------

So a quick recap of what we've done before we move on. We've created a `List`
database model and a `ModelDataMapper` that maps our Python models to JSON and
vice-versa. We've created a ListListView, which handles both GETing all our
List instances in the database and POSTing new instances to our database. We've
also then mapped our /api/list/ url to that view which allows external clients
to use our API.

Not bad huh? We'll repeat the process and write view classes and corresponding
url patterns for the other endpoints that we defined earlier.

Writing the views: object of List
---------------------------------

We're now going to write the view that will return a single instance of a List
object. Similar to how we used the ``nap.rest.views.BaseListView`` mixin when
writing our list of List view, we're now going to use the BaseObjectView mixin.
The BaseObjectView combines ObjectMixin (which extends Django's
SingleObjectMixin) with View. From the Django docs: "SingleObjectMixin provides
a mechanism for looking up an object associated with the current HTTP request."
Again, this sounds like what we need!

Lets add the following code to the todoapp/rest_views.py file:

.. code:: python

    from nap.rest import views

    from . import mappers
    from . import models


    class ListObjectView(views.BaseObjectView):
        model = models.List
        mapper_class = mappers.ListMapper


Adding GET functionality: object of List
----------------------------------------

You should be getting a lot more comfortable with how nap uses the Django
Class-Based View. Lets add GET functionality to our ListObjectView. In a
similar fashion to how we have done throughout this tutorial we'll simply
include one of the powerful mixins. Namely, the ListObjectView mixin.

The todoapp/rest_views.py file should now look like this:

.. code:: python

    from nap import auth
    from nap.rest import views

    from . import mappers
    from . import models


    class ListListView(views.ListPostMixin, views.ListGetMixin, views.BaseListView):
        model = models.List
        mapper_class = mappers.ListMapper


    class ListObjectView(views.ObjectGetMixin, views.BaseObjectView):
        model = models.List
        mapper_class = mappers.ListMapper


Defining the URL: object of List
--------------------------------

Lets quickly add a URL to actually call this view and then we can test to
actually see if it works.

Add this url to your todoapp/urls.py file:

.. code-block:: python

    url(r'^list/(?P<pk>\d+)/$', csrf_exempt(rest_views.ListObjectView.as_view())),

Again we're using the csrf_exempt() decorator for the sake of this tutorial.

Testing: object of List
-----------------------

We are only allowing the HTTP GET verb to be used with this view. That means we
don't need to use Requests (although you certainly could) to test it. All you
need to do is access the url we defined above with your web browser. Let's do
just that and access the following url: http://127.0.0.1:8000/api/list/1/.

A quick explanation of what's happening here: the /1/ component of your URL
corresponds to the (?P<pk>\d+) regular expression in the url tuple. You can
change the value of the pk component to retrieve an individual object view of
any List instance. At this stage there's not much in a detail view - only the
List title, but we're going to go on and add a bit more content next.

Quick pass through views for Item
---------------------------------

So far we've built the GET and POST functionality for our List resource. You
should be able to replicate the process we went through above and build GET and
POST functionality for the Item resource yourself. I'm going to paste the code
for that below, but I recommend you try do it yourself first! Note, the code
below excludes the more complicated foreign key fields which we will build
together.

Add the following to todoapp/rest_views.py:

.. code-block:: python

    class ItemListView(views.ListPostMixin, views.ListGetMixin, views.BaseListView):
        model = models.Item
        mapper_class = mappers.ItemMapper


    class ItemObjectView(views.ObjectGetMixin, views.BaseObjectView):
        model = models.Item
        mapper_class = mappers.ItemMapper

Don't forget to update todoapp/urls.py with the URL tuples that will call these
views:

.. code-block:: python

    url(r'^item/$', csrf_exempt(rest_views.ItemListView.as_view())),
    url(r'^item/(?P<pk>\d+)/$', csrf_exempt(rest_views.ItemObjectView.as_view())),


5. Update Mappers
=================

Lets start modifying our `DataMappers` so that we can serialise any extra
fields, including related field sets and Foreign Key fields.

ListMapper: List item_set()
---------------------------

If we were writing a client application to consume the /api/list/ API endpoint,
we would probably want to include all of the Item's that are in a List.
Essentially that means we want to define a proxy field on the model, which
means we're going to add another field called ``items`` to our DataMapper.

Your ListMapper class in todoapp/mappers.py should look like this now:

.. code-block:: python

    class ListMapper(datamapper.ModelDataMapper):
        class Meta:
            model = models.List
            fields = '__all__'

        @datamapper.field
        def items(self):
            'Produces a list of dicts with pk and title.'
            return self.item_set.all()

You can see that we are using the ``field`` decorator to provide the get
functionality we want. If you try to access the
http://127.0.0.1:8000/api/list/1/ URL though, you'll notice Django raises a
TypeError: ``Item is not JSON serializable``. So we're going to use a handy
shortcut and cast our item_set into a Python list.

Change the return line of the item so that your class looks like this:

.. code-block:: python

    class ListMapper(datamapper.ModelDataMapper):
        class Meta:
            model = models.List
            fields = '__all__'

        @datamapper.field
        def items(self):
            'Produces a list of dicts with pk and title.'
            return list(
                self.item_set.values()
            )

This will return a list of Item dictionaries -
``[{<Item>},{<Item>} ... {<Item>}]``.
Lets get rid of all the excess Item data and only return the pk's and and
title's, change our queryset definition to this:
``self.item_set.values('pk', 'title')``.

ItemMapper: get/set an owner (User)
-----------------------------------

When we create an Item object (via an HTTP POST) we will pass it an id value
which represents the primary key of the User who owns it. That means we need to
update our ItemMapper and tell it how to set the owner field (User foreign
key). Again we'll use the ``field`` decorator to provide the get functionality
we want.

Update your ItemMapper in todoapp/mappers.py to look like this:

.. code-block:: python

    class ItemMapper(datamapper.ModelDataMapper):
        class Meta:
            model = models.Item
            fields = '__all__'
            exclude = ['owner', 'list']

        @datamapper.field
        def owner_id(self):
            return self.owner_id

We're now telling the DataMapper to include an owner_id field in the JSON
representation of an Item, and to return the owner_id (which is the primary key
of the owner field). Lets also now add the set functionality for this field.
This will tell the DataMapper how to take a JSON payload with an owner_id value
and actually set the owner field on the model instance. Again we'll use the
built in decorators to perform this, we'll use the ``setter`` decorator to
provide the set functionality.

Update your ItemMapper in todoapp/mappers.py to look like this:

.. code-block:: python

    class ItemMapper(datamapper.ModelDataMapper):
        class Meta:
            model = models.Item
            fields = '__all__'
            exclude = ['owner', 'list']

        @datamapper.field
        def owner_id(self):
            return self.owner_id

        @owner_id.setter
        def owner_id(self, value):
            try:
                self.owner = User.objects.get(pk=value)
            except models.User.DoesNotExist:
                raise ValidationError("Invalid owner_id")

Recap
-----

You can see that we have modified our `DataMappers` to use the ``field`` and
``setter`` decorators to provide the get/set functionality. The ``field``
decorator extends the builtin ``property``, and so supports ``@x.setter`` and
``@x.deleter`` for setting the setter and deleter functions.


6. Authorisation
================

nap does not provide authentication, but it is very easy to combine nap with
Django's authentication system, or any other third party authentication
applications.

nap does provide authorisation through a ``permit`` decorator. You can use it
to control the permissions of any handler method. We're going to create a login
view that will authorise a user using the Django authentication system. This
means we'll be able to make use of Django's inbuilt forms too.

In your rest_views.py add the following class:

.. code-block:: python

    from django.contrib import auth as django_auth # Don't forget this
    from django.contrib.auth.forms import AuthenticationForm # Don't forget this

    from nap import http # Don't forget this


    class LoginView(views.BaseObjectView):
        mapper_class = mappers.UserMapper

        def get(self, request):
            if request.user.is_authenticated():
                return self.single_response(object=request.user)
            return http.Forbidden()

        def post(self, request):
            if request.user.is_authenticated():
                django_auth.logout(request)
                return self.get(request)
            form = AuthenticationForm(request, self.get_request_data())
            if form.is_valid():
                django_auth.login(request, form.get_user())
                return self.get(request)
            return self.error_response(form.errors)


We have defined a BaseObjectView that will allow get() and post(). If logged
in, GET will return a serialised representation of the User, and if not logged
in will return an HTTP 403. If not logged in, POST will authenticate the User
and either log them in, or return an error dictionary. POSTing to this view
when already logged in will log the User out.

7. Permissions
==============

Now that we have created an authorisation endpoint and view, we can decorate
some of our views to control permissions to them. This is achieved by using the
``permit`` decorator.

We've decided we only want to allow logged in users to post new messages, so we
override post() method of the ListListView class which is provided by the
ListPostMixin class. Permissions can be set on a per method basis, for example
the following set-up will allow POSTing only if authorised.

.. code-block:: python

    from nap import auth
    from nap.rest import views

    from . import mappers
    from . import models


    class ListListView(views.ListPostMixin, views.ListGetMixin, views.BaseListView):
        model = models.List
        mapper_class = mappers.ListMapper

        @auth.permit_logged_in
        def post(self, *args, **kwargs):
            return super(ListListView, self).post(*args, **kwargs)

Let's update our Item related views to only allow authorised Users to GET and
POST. We'll override the get() and post() methods for the ItemListView.

Update the ItemListView class in todoapp/rest_views.py to look like this:

.. code-block:: python

    class ItemListView(views.ListPostMixin, views.ListGetMixin, views.BaseListView):
        model = models.Item
        mapper_class = mappers.ItemMapper

        @auth.permit_logged_in
        def get(self, *args, **kwargs):
            return super(ItemListView, self).get(*args, **kwargs)

        @auth.permit_logged_in
        def post(self, *args, **kwargs):
             return super(ItemListView, self).get(*args, **kwargs)

Next we'll override the get() method of the ItemObjectView class. Update the
ItemObjectView class in todoapp/rest_views.py to look like this:

.. code-block:: python

    class ItemObjectView(views.ObjectGetMixin, views.BaseObjectView):
        model = models.Item
        mapper_class = mappers.ItemMapper

        @auth.permit_logged_in
        def get(self, *args, **kwargs):
            return super(ItemObjectView, self).get(*args, **kwargs)

8. Finished!
============

Well done. We've finished building our API service!
