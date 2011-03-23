# -*- coding: utf-8 -*-
__license__ = "GNU Affero General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

# This file is part of Kirinki.
# 
# Kirinki is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as 
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# Kirinki is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public
# License along with kirinki. If not, see <http://www.gnu.org/licenses/>.

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
