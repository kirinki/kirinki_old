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

from kirinki.index import IndexView
from kirinki.user import LoginView, LogoutView, RegisterView, ActivationView, AdminView, AccountView
from kirinki.videos import StreamingView, VideosView, StreamView, UploadView

# @vary_on_header s('Cookie')
# @cache_control(private=True, must_revalidate=True, max_age=3600)
@never_cache
@vary_on_cookie
def index(request):
    return IndexView(request).getRender()

@user_passes_test(lambda u: u.is_anonymous(),'index')
def auth_login(request):
    return LoginView(request).getRender()
    
@user_passes_test(lambda u: u.is_authenticated(),'index')
def auth_logout(request):
    return LogoutView(request).getRender()

@user_passes_test(lambda u: u.is_anonymous(),'index')
def reg(request):
    return RegisterView(request).getRender()

@user_passes_test(lambda u: u.is_anonymous(),'index')
def activate(request, key):
    return ActivationView(request, key).getRender()

def streaming(request):
    return StreamingView(request).getRender()

def videos(request):
    return VideosView(request).getRender()

def viewVideo(request,key):
    return VideosView(request,VideosView.VIEW,key).getRender()

def deleteVideo(request,key):
    return VideosView(request,VideosView.DELETE,key).getRender()

@user_passes_test(lambda u: u.is_authenticated(),'index')
def stream(request):
    return StreamView(request).getRender()

@user_passes_test(lambda u: u.is_authenticated(),'index')
def upload(request):
    return UploadView(request).getRender()

@user_passes_test(lambda u: u.is_superuser,'index')
def admin(request):
    return AdminView(request).getRender()

@user_passes_test(lambda u: u.is_authenticated(),'index')
def account(request):
    return AccountView(request).getRender()
