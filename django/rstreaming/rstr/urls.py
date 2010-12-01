# from django.views.decorators.cache import cache_page
from django.conf.urls.defaults import *

urlpatterns = patterns('rstr.views',
                       (r'^/*$', 'index'),
                       (r'^/index/*$', 'index'),
                       (r'^index/*$', 'index'),
                       (r'^login/*$', 'auth_login'),
                       (r'^logout/*$', 'auth_logout'),
                       (r'^about/*$', 'about'),
                       (r'^register/*$', 'reg'),
                       # (r'^/*$', cache_page('index',60*5)), # Vista cacheada 5 minutos
                       # (r'^$(?P<parametro>\d+)/$', 'index'),
                       )
