from django.conf.urls import patterns, include
from . import rpc_views
from . import rest_views

#from nap.rest import api
#api.autodiscover()

urlpatterns = patterns('',
#    (r'^api/', include(api.patterns(True))),
    (r'^rpc/', rpc_views.View.as_view()),
    (r'^rest/polls/(?P<pk>\d+)$', rest_views.SinglePollView.as_view()),
)
