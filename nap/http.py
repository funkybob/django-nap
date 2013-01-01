
'''Add some missing HttpResponse sub-classes'''
from django.http import *

from functools import partial

HttpCreated = partial(HttpResponse, status_code=201)
HttpAccepted = partial(HttpResponse, status_code=202)
HttpNoContent = partial(HttpResponse, status_code=204)
HttpResetContent = partial(HttpResponse, status_code=205)
HttpPartialContent = partial(HttpResponse, status_code=206)

from utils import JSONEncoder

json = JSONEncoder()

class JsonResponse(HttpResponse):
    '''Handy shortcut for dumping JSON data'''
    def __init__(self, content, *args, **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        super(JsonResponse, self).__init__(json.dumps(content), *args, **kwargs)

