
class ValidationError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):  # pragma: no cover
        return 'ValidationError: %s' % self.message


class ValidationErrors(Exception):
    '''A container for a dict of validation errors.'''
    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        return 'ValidationErrors: %s' % (
            '\n'.join('%s: %s' % (
                (key, map(str, value))
                for key, value in self.errors.items()
            )),
        )
