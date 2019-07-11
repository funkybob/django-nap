
'''
A wrapper for django shortcuts that adapts responses to be from nap.http
'''

from django.shortcuts import _get_queryset

from nap import http


def get_object_or_404(klass, *args, **kwargs):
    """
    Uses get() to return an object, or raises a NotFound exception if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more
    han one object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise http.NotFound()


def get_list_or_404(klass, *args, **kwargs):
    """
    Uses filter() to return a list of objects, or raise a NotFound exception if
    the list is empty.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the filter() query.
    """
    queryset = _get_queryset(klass)
    obj_list = list(queryset.filter(*args, **kwargs))
    if not obj_list:
        raise http.NotFound()
    return obj_list
