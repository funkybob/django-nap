

# TODO: Add other patterns to allow introspection?

class Api(object):
    '''Helper class for registering many Publishers in one URL namespace'''
    def __init__(self, name):
        self.name = name
        self.children = {}

    def patterns(self):
        urlpatterns = []
        for child in self.children:
            urlpatterns.extend(child.patterns())
        return [
            (r'^%s/' % self.name, include([
                (r'^%s/' % name, include(child.patterns()))
                for name, child in self.children.items()
            ]))
        ]

    def register(self, child, name=None):
        if name is None:
            name = getattr(child, 'api_name', child.__class__.__name__.lower())
        if name in self.children:
            raise Warning('Publisher with name %s already registered: %r -> %r' % (
                name, self.children[name], child
            ))
        self.children[name] = child

