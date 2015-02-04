
class ContentTypeError(TypeError):
    pass


class Encoder(object):

    CONTENT_TYPES = []

    def __init__(self, content_type, content_data):
        if content_type not in self.CONTENT_TYPES:
            raise ContentTypeError()

        self.content_type = content_type
        self.content_data = content_data

    def encode(self, data):
        '''
        Returns (encoded data, content_type)
        '''
        raise NotImplementedError

    def decode(self, data):
        raise NotImplementedError


def find_encoder(request, encoders):
    content_type, content_data = parse_header(request.META.get('CONTENT_TYPE', ''))

    for encoder in encoders:
        try:
            enc = encoder(content_type, content_data)
        except ContentTypeError:
            continue
        else:
            return enc

    return None
