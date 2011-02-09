# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

# from django.views.decorators.cache import cache_page
from django.conf.urls.defaults import *

urlpatterns = patterns('kirinki.views',
                       (r'^/*$', 'indexView'),
                       (r'^index/*$', 'indexView'),
                       (r'^/index/*$', 'indexView'),
                       (r'^login/*$', 'loginView'),
                       (r'^logout/*$', 'logoutView'),
                       (r'^register/*$', 'registerView'),
                       (r'^streaming/*$', 'streamingView'),
                       (r'^streaming/reference/*$', 'referenceStreamingView'),
                       (r'^videos/*$', 'videosView'),
                       (r'^videos/view/(?P<key>\d+)/*$', 'viewVideoView'),
                       (r'^videos/delete/(?P<key>\d+)/*$', 'deleteVideoView'),
                       (r'^videos/reference/(?P<key>\d+)/*$', 'referenceVideoView'),
                       (r'^stream/*$', 'streamView'),
                       (r'^upload/*$', 'uploadView'),
                       (r'^administrator/*$', 'adminView'),
                       (r'^account/*$', 'accountView'),
                       (r'^account/confirm/(?P<key>\w+)/*$', 'activateView'),
                       # (r'^/*$', cache_page('index',60*5)), # Vista cacheada 5 minutos
                       # (r'^$(?P<parametro>\d+)/$', 'index'),
                       )
