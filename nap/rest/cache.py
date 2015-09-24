from __future__ import unicode_literals

from django.core.cache import cache as default_cache
from django.core.cache import get_cache
from django.utils.six import string_types


class CachedSerialiser(object):
    '''Mixin to cache per-object serialised data'''
    def __init__(self, *args, **kwargs):
        cache = getattr(self._meta, 'cache', default_cache)
        if isinstance(cache, string_types):
            cache = get_cache(cache)
        self._meta.cache = cache

    def object_deflate(self, obj, **kwargs):
        '''Add object caching'''
        # This currently assumes obj is a Model instance
        cache_key = 'api_%s_%d' % (self.__class__.__name__, obj.pk)
        data = self._meta.cache.get(cache_key)
        if data is None:
            data = super(CachedSerialiser, self).object_deflate(obj, **kwargs)
            timeout = getattr(self._meta, 'timeout', None)
            self._meta.cache.set(data, timeout=timeout)
        return data
