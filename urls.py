from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^$', 'django.views.generic.simple.direct_to_template',
     {'template': 'home.html'})
)

urlpatterns += patterns('journalists.views',
    ('^journalists/list/$', 'listJournalists'),
    ('^journalists/new/$', 'newJournalist'),
    ('^journalist/(?P<id>\d+)/$', 'viewJournalist'),
    ('^journalist/(?P<slug>[a-z0-9-]+)/$', 'viewJournalist'),
    ('^journalist/(?P<id>\d+)/edit/$', 'editJournalist'),
    ('^journalist/(?P<slug>[a-z0-9-]+)/edit/$', 'editJournalist'),
    ('^journalist/(?P<id>\d+)/publishing/edit/$', 'editPublishing'),
    ('^journalist/(?P<slug>[a-z0-9-]+)/publishing/edit/$', 'editPublishing')
)

urlpatterns += patterns('publishers.views',
    ('^publishers/list/$', 'listPublishers'),
    ('^publishers/new/$', 'editPublisher'),
    ('^publisher/(?P<id>\d+)/edit/$', 'editPublisher'),
    ('^publisher/(?P<slug>[a-z0-9-]+)/edit/$', 'editPublisher'),
)
