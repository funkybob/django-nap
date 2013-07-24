from django.conf.urls import patterns, include
from nap import api

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
api.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include(api.patterns(True))),
)
