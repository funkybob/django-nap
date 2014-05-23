
from django.apps import AppConfig

from django.utils.module_loading import autodiscover_modules

from . import api

class NapConfig(AppConfig):
    '''App Config that performs auto-discover on ready.'''

    def ready(self):
        super(NapConfig, self).ready()
        autodiscover_modlues('publishers')
