# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

# from django.views.decorators.cache import cache_page
from django.conf.urls.defaults import *

urlpatterns = patterns('rstr.views',
                       (r'^/*$', 'index'),
                       (r'^index/*$', 'index'),
                       (r'^/index/*$', 'index'),
                       (r'^login/*$', 'auth_login'),
                       (r'^logout/*$', 'auth_logout'),
                       (r'^register/*$', 'reg'),
                       (r'^streaming/*$', 'streaming'),
                       (r'^videos/*$', 'videos'),
                       (r'^videos/(?P<key>\d+)/*$', 'viewVideo'),
                       (r'^stream/*$', 'stream'),
                       (r'^upload/*$', 'upload'),
                       (r'^admin/*$', 'admin'),
                       (r'^account/*$', 'account'),
                       (r'^account/confirm/(?P<key>\w+)/*$', 'activate'),
                       # (r'^/*$', cache_page('index',60*5)), # Vista cacheada 5 minutos
                       # (r'^$(?P<parametro>\d+)/$', 'index'),
                       )
