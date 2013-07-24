
from django.contrib import admin

from . import models

admin.site.register(models.Poll)
admin.site.register(models.Choice)
