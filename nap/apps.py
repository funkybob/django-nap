
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class NapConfig(AppConfig):
    '''App Config that performs publisher auto-discover on ready.'''

    name = 'nap'

    def ready(self):
        autodiscover_modules('publishers')
