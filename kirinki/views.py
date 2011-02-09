# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

import logging

from django.views.decorators.vary import vary_on_cookie
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import user_passes_test
# from django.views.decorators.vary import vary_on_headers
# from django.views.decorators.cache import cache_control

from kirinki.index import IndexController
from kirinki.user import LoginController, LogoutController, RegisterController, ActivationController, AdminController, AccountController
from kirinki.videos import StreamingController, VideoController, StreamController, UploadController

# @vary_on_header s('Cookie')
# @cache_control(private=True, must_revalidate=True, max_age=3600)
@never_cache
@vary_on_cookie
def indexView(request):
    return IndexController(request).getRender()

@user_passes_test(lambda u: u.is_anonymous(),'index')
def loginView(request):
    return LoginController(request).getRender()
    
@user_passes_test(lambda u: u.is_authenticated(),'index')
def logoutView(request):
    return LogoutController(request).getRender()

@user_passes_test(lambda u: u.is_anonymous(),'index')
def registerView(request):
    return RegisterController(request).getRender()

@user_passes_test(lambda u: u.is_anonymous(),'index')
def activateView(request, key):
    return ActivationController(request, key).getRender()

def streamingView(request):
    return StreamingController(request).getRender()

def referenceStreamingView(request):
    return StreamingController(request).getRender()

def videosView(request):
    return VideoController(request).getRender()

def viewVideoView(request,key):
    return VideoController(request,VideoController.VIEW,key).getRender()

def deleteVideoView(request,key):
    return VideoController(request,VideoController.DELETE,key).getRender()

def referenceVideoView(request,key):
    return VideoController(request,VideoController.REFERENCE,key).getRender()

@user_passes_test(lambda u: u.is_authenticated(),'index')
def streamView(request):
    return StreamController(request).getRender()

@user_passes_test(lambda u: u.is_authenticated(),'index')
def uploadView(request):
    return UploadController(request).getRender()

@user_passes_test(lambda u: u.is_superuser,'index')
def adminView(request):
    return AdminController(request).getRender()

@user_passes_test(lambda u: u.is_authenticated(),'index')
def accountView(request):
    return AccountController(request).getRender()
