from django.conf.urls.defaults import patterns, url
from openstack_dashboard.dashboards.microserver.recipes import views
from .views import IndexView


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    #url(r'^recipes/new/(s)$')
    url(r'^create/$', views.CreateView.as_view(), name='create'),
    url(r'^(?P<id>[^/]+)/update/$', views.UpdateView.as_view(), name='update'),
)
