from __future__ import unicode_literals

from django.conf.urls import include, url
from django.core.urlresolvers import reverse

from .. import http


class Api(object):
    '''Helper class for registering many Publishers in one URL namespace'''
    def __init__(self, name, show_index=True):
        self.name = name
        self.children = {}
        self.show_index = show_index

    def patterns(self, flat=False):
        urlpatterns = [
            url(r'^$', self.index),
        ] + [
            url(r'^%s/' % name, include(child.patterns(self.name)))
            for name, child in self.children.items()
        ]
        if flat:
            return urlpatterns
        return [
            url(r'^%s/' % self.name, include(urlpatterns)),
        ]

    def index(self, request, *args, **kwargs):
        '''Return a dict of publisher name: url'''
        if not self.show_index:
            return http.NotFound()
        return http.JsonResponse(dict(
            (name, {
                'path': reverse(
                    '%s_%s_list_default' % (self.name, name),
                    kwargs=kwargs
                ),
                'methods': child.index(),
            })
            for name, child in self.children.items()
        ))

    def register(self, child, name=None):
        if name is None:
            name = getattr(child, 'api_name', child.__name__.lower())
        if name in self.children:
            raise Warning(
                'Publisher with name "%s" already registered: %r -> %r' % (
                    name, self.children[name], child
                )
            )
        self.children[name] = child

APIS = {}


def register(name, *args):
    if not args:
        # We've been called as a decorator
        def wrapper(cls, name=name):
            register(name, cls)
            return cls
        return wrapper
    try:
        api = APIS[name]
    except KeyError:
        api = APIS[name] = Api(name=name)
    for resource in args:
        api.register(resource)
    return api


def autodiscover():
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's api module.
        try:
            import_module('%s.publishers' % app)
        except:

            # Decide whether to bubble up this error. If the app just
            # doesn't have an admin module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'publishers'):
                raise


def patterns(flat=False):
    urlpatterns = []
    for api in APIS.values():
        urlpatterns.extend(api.patterns(flat=flat))
    return urlpatterns
