# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

# from django.views.decorators.vary import vary_on_headers
from django.views.decorators.vary import vary_on_cookie
# from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from rstr.config import Config
from rstr.mainviewer import MainViewer
from rstr.index import IndexView
from rstr.user import LoginView
from rstr.user import LogoutView
from rstr.user import RegisterView
from rstr.user import ActivationView
import logging

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
    return ActivationView(request).getRender()

def streaming(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    messages.set_level(request, messages.INFO)
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session).getSessionData()
        request.session.update(data)
        request.session['isConfig'] = True
    return MainViewer(request).getViewer('streaming')

def videos(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    messages.set_level(request, messages.INFO)
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session).getSessionData()
        request.session.update(data)
        request.session['isConfig'] = True
    return MainViewer(request).getViewer('videos')

@user_passes_test(lambda u: u.is_authenticated(),'index')
def stream(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    messages.set_level(request, messages.INFO)
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session).getSessionData()
        request.session.update(data)
        request.session['isConfig'] = True
    return MainViewer(request).getViewer('upload')

@user_passes_test(lambda u: u.is_superuser,'index')
def admin(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    messages.set_level(request, messages.INFO)
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session).getSessionData()
        request.session.update(data)
        request.session['isConfig'] = True
    return MainViewer(request).getViewer('admin')

@user_passes_test(lambda u: u.is_authenticated(),'index')
def account(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    messages.set_level(request, messages.INFO)
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session).getSessionData()
        request.session.update(data)
        request.session['isConfig'] = True
    return MainViewer(request).getViewer('account')
