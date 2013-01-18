from django.conf.urls import patterns, include

from nap import api
api.autodiscover()

urlpatterns = patterns('',
    (r'^api/', include(api.patterns(True))),
)
