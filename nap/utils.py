
import json
from decimal import Decimal
import datetime

def digattr(obj, attr, default=None):
    '''Perform template-style dotted lookup'''
    steps = attr.split('.')
    for step in steps:
        try:    # dict lookup
            obj = obj[step]
        except (TypeError, AttributeError, KeyError):
            try:    # attribute lookup
                obj = getattr(obj, step)
            except (TypeError, AttributeError):
                try:    # list index lookup
                    obj = obj[int(step)]
                except (IndexError, ValueError, KeyError, TypeError):
                    return default
        if callable(obj):
            obj = obj()
    return obj

def undigattr(obj, attr, value):
    steps = attr.split('.')
    steps.reverse()
    last = steps.pop(0)
    for step in steps:
        try:
            obj = obj[step]
        except (TypeError, AttributeError, KeyError):
            try:    # attribute lookup
                obj = getattr(obj, step)
            except (TypeError, AttributeError):
                try:    # list index lookup
                    obj = obj[int(step)]
                except (IndexError, ValueError, KeyError, TypeError):
                    return default
        if callable(obj):
            obj = obj()
    setattr(obj, last, value)

from django.db.models import Model

class JSONEncoder(json.JSONEncoder):
    '''
    Same features as JSONEncoder, but not as a generator.
    '''
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            return '"' + obj.replace(microsecond=0).isoformat(' ') + '"'
        if isinstance(obj, datetime.date):
            return '"' + obj.isoformat() + '"'
        if hasattr(obj, '__iter__'):
            return list(obj)
        if isinstance(obj, Model):
            return unicode(obj)
        return super(JSONEncoder, self).default(obj)
