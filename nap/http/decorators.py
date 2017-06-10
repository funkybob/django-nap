from . import BaseHttpResponse


class except_response:
    '''
    Allow view functions to handle HttpResponse as exception.
    '''
    def __init__(self, func):
        self.func = func

    def __call__(self, request, *args, **kwargs):
        try:
            return self.func(request, *args, **kwargs)
        except BaseHttpResponse as resp:
            return resp
