
'''Add some missing HttpResponse sub-classes'''
from django.http import *

from functools import partial

HttpCreated = partial(HttpResponse, status_code=202)
HttpNoContent = partial(HttpResponse, status_code=204)

