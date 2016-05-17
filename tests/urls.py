from django.conf.urls import include, url
from . import rpc_views
from . import rest_views

from nap.rest import api
#api.autodiscover()

urlpatterns = [
    url(r'^api/', include(api.patterns(True))),
    url(r'^rpc/', rpc_views.View.as_view()),
    url(r'^rest/polls/(?P<pk>\d+)$', rest_views.SinglePollView.as_view()),
    url(r'^rest/polls/$', rest_views.PollListView.as_view()),
]
