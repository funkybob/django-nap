

# TODO: Add other patterns to allow introspection?

class Api(object):
    '''Helper class for registering many Publishers in one URL namespace'''
    def __init__(self, name):
        self.name = name
        self.children = set()

    def patterns(self):
        urlpatterns = []
        for child in self.children:
            urlpatterns.extend(child.patterns())
        return [
            (r'^%s/' % self.name, include(urlpatterns))),
        ]

    def register(self, child):
        self.children.add(child)

