
from django.conf.urls import url, include

# TODO: Add other patterns to allow introspection?

class Api(object):
    '''Helper class for registering many Publishers in one URL namespace'''
    def __init__(self, name):
        self.name = name
        self.children = {}

    def patterns(self, flat=False):
        urlpatterns = [
            url(r'^%s/' % name, include(child.patterns()))
            for name, child in self.children.items()
        ]
        if flat:
            return urlpatterns
        return [
            url(r'^%s/' % self.name, include(urlpatterns)),
        ]

    def register(self, child, name=None):
        if name is None:
            name = getattr(child, 'api_name', child.__class__.__name__.lower())
        if name in self.children:
            raise Warning('Publisher with name %s already registered: %r -> %r' % (
                name, self.children[name], child
            ))
        self.children[name] = child

APIS = {}

def register(name, *args):
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
            import_module('%s.serialiser' % app)
        except:

            # Decide whether to bubble up this error. If the app just
            # doesn't have an admin module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'serialiser'):
                raise

def patterns(flat=False):
    patterns = []
    for api in APIS.values():
        patterns.extend(api.patterns(flat=flat))
    return patterns

