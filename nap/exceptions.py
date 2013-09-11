
class ValidationError(Exception):
    def __init__(self, message):
        self.message = message

    def __unicode__(self):
        return self.message


class ValidationErrors(Exception):
    '''A container for a dict of validation errors.'''
    def __init__(self, errors):
        self.errors = errors
