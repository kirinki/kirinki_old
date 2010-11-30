# from django.views.decorators.cache import cache_page
from django.conf.urls.defaults import *

urlpatterns = patterns('rstr.views',
                       # (r'^/*$', cache_page('index',60*5)), # Vista cacheada 5 minutos
                       (r'^/*$', 'index'),
                       (r'^/index/*$', 'index'),
                       # (r'^$(?P<parametro>\d+)/$', 'index'),
                       )
