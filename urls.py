from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^$', 'django.views.generic.simple.direct_to_template',
     {'template': 'home.html'})
)

urlpatterns += patterns('journalists.views',
    ('^journalists/list/$', 'listJournalists'),
    ('^journalists/new/$', 'editJournalist'),
    ('^journalist/(?P<id>\d+)/edit/$', 'editJournalist'),
    ('^journalist/(?P<slug>.+)/edit/$', 'editJournalist'),
    ('^journalist/(?P<id>\d+)/$', 'viewJournalist'),
    ('^journalist/(?P<slug>.+)/$', 'viewJournalist'),
)
