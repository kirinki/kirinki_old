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
        data = Config(request.session.session_key).getSessionData()
        request.session.update(data)
        request.session['isConfig'] = True
    return MainViewer(request, request.session.session_key).getViewer('index')

@user_passes_test(lambda u: u.is_anonymous(),'index')
def auth_login(request):
    if request.method == 'POST':
        if request.session['user'].is_authenticated():
            messages.add_message(request, messages.ERROR, 'User already logged in')
            if request.META.get('HTTP_REFERER', False) is not False:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                return HttpResponse(reverse('index'))
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
                    return HttpResponse(reverse('index'))
            else:
                # Return a 'disabled account' error message
                messages.add_message(request, messages.ERROR, 'Your account is disabled.')
                if request.META.get('HTTP_REFERER', False) is not False:
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])
                else:
                    return HttpResponse(reverse('index'))
        else:
            # Return an 'invalid login' error message.
            messages.add_message(request, messages.ERROR, 'Username or password error.')
            if request.META.get('HTTP_REFERER', False) is not False:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                return HttpResponse(reverse('index'))
    elif request.method == 'GET':
        logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
        messages.set_level(request, messages.INFO)
        if request.session.get('isConfig', False) is False:
            request.session.set_expiry(600)
            data = Config(request.session.session_key).getSessionData()
            request.session.update(data)
            request.session['isConfig'] = True
        return MainViewer(request, request.session.session_key).getViewer('login')
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
            return HttpResponse(reverse('index'))
    else:
        messages.add_message(request, messages.ERROR, 'User not logged in.')
        if request.META.get('HTTP_REFERER', False) is not False:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponse(reverse('index'))

def about(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    messages.set_level(request, messages.INFO)
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session.session_key).getSessionData()
        request.session.update(data)
        request.session['isConfig'] = True
    return MainViewer(request, request.session.session_key).getViewer('about')

@user_passes_test(lambda u: u.is_anonymous(),'index')
def reg(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    if request.method == 'GET':
        messages.set_level(request, messages.INFO)
        if request.session.get('isConfig', False) is False:
            request.session.set_expiry(600)
            data = Config(request.session.session_key).getSessionData()
            request.session.update(data)
            request.session['isConfig'] = True
        return MainViewer(request, request.session.session_key).getViewer('register')
    elif request.method == 'POST':
        messages.set_level(request, messages.INFO)
        if request.session.get('isConfig', False) is False:
            request.session.set_expiry(600)
            data = Config(request.session.session_key).getSessionData()
            request.session.update(data)
            request.session['isConfig'] = True
        return MainViewer(request, request.session.session_key).getViewer('register')
    else:
        raise Http404

def streaming(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    messages.set_level(request, messages.INFO)
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session.session_key).getSessionData()
        request.session.update(data)
        request.session['isConfig'] = True
    return MainViewer(request, request.session.session_key).getViewer('streaming')

def videos(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    messages.set_level(request, messages.INFO)
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session.session_key).getSessionData()
        request.session.update(data)
        request.session['isConfig'] = True
    return MainViewer(request, request.session.session_key).getViewer('videos')

@user_passes_test(lambda u: u.is_authenticated(),'index')
def stream(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    messages.set_level(request, messages.INFO)
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session.session_key).getSessionData()
        request.session.update(data)
        request.session['isConfig'] = True
    return MainViewer(request, request.session.session_key).getViewer('stream')

@user_passes_test(lambda u: u.is_authenticated(),'index')
def upload(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    messages.set_level(request, messages.INFO)
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session.session_key).getSessionData()
        request.session.update(data)
        request.session['isConfig'] = True
    return MainViewer(request, request.session.session_key).getViewer('upload')

@user_passes_test(lambda u: u.is_superuser,'index')
def admin(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    messages.set_level(request, messages.INFO)
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session.session_key).getSessionData()
        request.session.update(data)
        request.session['isConfig'] = True
    return MainViewer(request, request.session.session_key).getViewer('admin')
