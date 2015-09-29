import datetime

from django.core.exceptions import ValidationError


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


class NotNullFilter(Filter):
    @staticmethod
    def to_python(value):
        if value is None:
            raise ValidationError('May not be null')
        return value


class BooleanFilter(Filter):
    @staticmethod
    def to_python(value):
        if value is None:
            return value
        if isinstance(value, bool):
            return value
        return value.lower() in (1, '1', 't', 'y', 'true')


class _CastFilter(Filter):
    @classmethod
    def to_python(self, value):
        if value is None or isinstance(value, self.type_class):
            return value
        try:
            return self.type_class(value)
        except ValueError as e:
            raise ValidationError(e.args[0])


class IntegerFilter(_CastFilter):
    type_class = int


class FloatFilter(_CastFilter):
    type_class = float


class TimeFilter(object):
    @staticmethod
    def to_python(value):
        if value is None or isinstance(value, datetime.time):
            return value
        return datetime.datetime.strptime(value, '%H:%M:%S').time()

    @staticmethod
    def from_python(value):
        if value is None:
            return value
        return value.replace(microsecond=0).isoformat()


class DateFilter(object):
    @staticmethod
    def to_python(value):
        if value is None or isinstance(value, datetime.date):
            return value
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()

    @staticmethod
    def from_python(value):
        if value is None:
            return value
        return value.isoformat()


class DateTimeFilter(object):
    @staticmethod
    def to_python(value):
        if value is None or isinstance(value, datetime.datetime):
            return value
        return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def from_python(value):
        if value is None:
            return value
        return value.replace(microsecond=0).isoformat(' ')
