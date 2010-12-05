# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

# from django.views.decorators.vary import vary_on_headers
from django.views.decorators.vary import vary_on_cookie
# from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from recaptcha.client import captcha
from django.core.mail import send_mail
from rstr.config import Config
from rstr.mainviewer import MainViewer
import logging

# @vary_on_header s('Cookie')
# @cache_control(private=True, must_revalidate=True, max_age=3600)
@never_cache
@vary_on_cookie
def index(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    messages.set_level(request, messages.INFO)
    # request.session.clear()
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session).getSessionData()
        request.session.update(data)
        request.session['isConfig'] = True
    return MainViewer(request, request.session).getViewer('index')

@user_passes_test(lambda u: u.is_anonymous(),'index')
def auth_login(request):
    if request.method == 'POST':
        if request.session['user'].is_authenticated():
            messages.add_message(request, messages.ERROR, 'User already logged in')
            if request.META.get('HTTP_REFERER', False) is not False:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                return HttpResponseRedirect('/rstr/index')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.INFO, 'User logged in')
                request.session['user'] = user
                if request.META.get('HTTP_REFERER', False) is not False:
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])
                else:
                    return HttpResponseRedirect('/rstr/index')
            else:
                # Return a 'disabled account' error message
                messages.add_message(request, messages.ERROR, 'Your account is disabled.')
                if request.META.get('HTTP_REFERER', False) is not False:
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])
                else:
                    return HttpResponseRedirect('/rstr/index')
        else:
            # Return an 'invalid login' error message.
            messages.add_message(request, messages.ERROR, 'Username or password error.')
            if request.META.get('HTTP_REFERER', False) is not False:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                return HttpResponseRedirect('/rstr/index')
    elif request.method == 'GET':
        logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
        messages.set_level(request, messages.INFO)
        if request.session.get('isConfig', False) is False:
            request.session.set_expiry(600)
            data = Config(request.session).getSessionData()
            request.session.update(data)
            request.session['isConfig'] = True
        return MainViewer(request, request.session).getViewer('login')
    else:
        raise Http404

@user_passes_test(lambda u: u.is_authenticated(),'index')
def auth_logout(request):
    if request.session['user'].is_authenticated():
        logout(request)
        messages.add_message(request, messages.INFO, 'User logged out.')
        if request.META.get('HTTP_REFERER', False) is not False:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseRedirect('/rstr/index')
    else:
        messages.add_message(request, messages.ERROR, 'User not logged in.')
        if request.META.get('HTTP_REFERER', False) is not False:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponse(reverse('logout'))

@user_passes_test(lambda u: u.is_anonymous(),'index')
def reg(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    if request.method == 'GET':
        if request.session.get('isConfig', False) is False:
            messages.set_level(request, messages.INFO)
            request.session.set_expiry(600)
            data = Config(request.session).getSessionData()
            request.session.update(data)
            request.session['isConfig'] = True
        return MainViewer(request, request.session).getViewer('register')
    elif request.method == 'POST':
        if request.POST['password'] != request.POST['repeat_password']:
            messages.add_message(request, messages.INFO, 'User not registered. Passwords doesn\'t match.')
        else:
            remote_ip = request.META['REMOTE_ADDR']
            challenge = request.REQUEST.get('recaptcha_challenge_field')
            response = request.REQUEST.get('recaptcha_response_field')
            recaptcha_response = captcha.submit(challenge, response, '6LefRr8SAAAAAPpY8WNoxo19nh0Rre5BCB9JfLJV', remote_ip)

            if recaptcha_response.is_valid:
                try:
                    User.objects.get(username=request.POST['username'])
                except User.DoesNotExist:
                    user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
                    user.is_active = False
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.groups.add(Group.object.get(name='users'))
                    user.save()

                    send_mail('Welcome to Ritho\'s Streaming!', 'Welcome to Ritho\'s Streaming!\nTo activate the account please visit http://turing.ritho.net/rstr/activate?id='+str(user.id), 'rstr@ritho.net', [ user.email ], fail_silently=False)
                
                    messages.add_message(request, messages.INFO, 'User registered. To activate the account please visit the url inicated in your email.')
            else:
                messages.add_message(request, messages.ERROR, 'User not registered. '+recaptcha_response.error_code)

            if request.session.get('isConfig', False) is False:
                messages.set_level(request, messages.INFO)
                request.session.set_expiry(600)
                data = Config(request.session).getSessionData()
                request.session.update(data)
                request.session['isConfig'] = True
            if request.META.get('HTTP_REFERER', False) is not False:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                return HttpResponseRedirect('/rstr/index')
    else:
        raise Http404

@user_passes_test(lambda u: u.is_anonymous(),'index')
def activate(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=request.GET['id'])
            if not user.is_active:
                user.is_active = True
                user.save()
                messages.add_message(request, messages.INFO, 'User '+user.username+' is activated')
            else:
                messages.add_message(request, messages.INFO, 'User '+user.username+' was already activated')
        except User.DoesNotExist:
                messages.add_message(request, messages.INFO, 'User does not exists')
        return HttpResponseRedirect('/rstr/index')


def streaming(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    messages.set_level(request, messages.INFO)
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session).getSessionData()
        request.session.update(data)
        request.session['isConfig'] = True
    return MainViewer(request, request.session).getViewer('streaming')

def videos(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    messages.set_level(request, messages.INFO)
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session).getSessionData()
        request.session.update(data)
        request.session['isConfig'] = True
    return MainViewer(request, request.session).getViewer('videos')

@user_passes_test(lambda u: u.is_authenticated(),'index')
def stream(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    messages.set_level(request, messages.INFO)
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session).getSessionData()
        request.session.update(data)
        request.session['isConfig'] = True
    return MainViewer(request, request.session).getViewer('stream')

@user_passes_test(lambda u: u.is_authenticated(),'index')
def upload(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    messages.set_level(request, messages.INFO)
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session).getSessionData()
        request.session.update(data)
        request.session['isConfig'] = True
    return MainViewer(request, request.session).getViewer('upload')

@user_passes_test(lambda u: u.is_superuser,'index')
def admin(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    messages.set_level(request, messages.INFO)
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session).getSessionData()
        request.session.update(data)
        request.session['isConfig'] = True
    return MainViewer(request, request.session).getViewer('admin')

@user_passes_test(lambda u: u.is_authenticated(),'index')
def account(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    messages.set_level(request, messages.INFO)
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session).getSessionData()
        request.session.update(data)
        request.session['isConfig'] = True
    return MainViewer(request, request.session).getViewer('account')
