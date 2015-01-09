from datetime import datetime


class Filter(object):
    '''
    Provides casting and validation functions for Fields.
    '''
    @staticmethod
    def to_python(value):
        return value

    @staticmethod
    def from_python(value):
        return value


class _CastFilter(Filter):
    def to_python(self, value):
        return self.type_class(value)


class IntegerFilter(_CastFilter):
    type_class = int


class FloatFilter(_CastFilter):
    type_class = float


class TimeFilter(object):
    @staticmethod
    def to_python(value):
        datetime.strptime(value, '%H:%M:%S').time()

    @staticmethod
    def from_python(value):
        return value.isoformat()


class DateFilter(object):
    @staticmethod
    def to_python(value):
        datetime.strptime(value, '%Y-%m-%d').date()

    @staticmethod
    def from_python(value):
        return value.isoformat()


class DateTimeFilter(object):
    @staticmethod
    def to_python(value):
        datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def from_python(value):
        return value.isoformat(' ')
