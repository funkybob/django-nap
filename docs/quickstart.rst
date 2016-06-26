Quick Start
===========

Nap has two methods of use, you can use the: Serialisers/Publisher or the
DataMapper/Views combinations.

DataMapper/Views Quick Start
----------------------------

1. Create a DataMapper for your Model in mappers.py

.. code-block:: python

    from nap import datamapper
    from myapp.models import MyModel

    class MyModelMapper(datamapper.ModelDataMapper):
        class Meta:
            model = MyModel
            exclude = ['user',]

2. Create some views in rest_views.py

.. code-block:: python

    from nap.rest import views

    class MyModelListView(views.ListPostMixin,
                           views.BaseListView):
        pass


    class MyModelObjectView(views.ObjectGetMixin,
                            views.BaseObjectView):
        pass

3. Add your APIs to your URLs:

.. code-block:: python

    urlpatterns = [
        url(r'^mymodel/$',
            MyModelListView.as_view(),
            name='mymodel-list'),

        url(r'^mymodel/(?P<pk>\d+)/$',
            MyModelObjectView.as_view(),
            name='mymodel-detail'),
    ]
