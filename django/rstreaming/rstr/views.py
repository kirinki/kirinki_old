from django.shortcuts import render_to_response
from django.template.loader import render_to_string
# from django.views.decorators.vary import vary_on_headers
from django.views.decorators.vary import vary_on_cookie
# from django.views.decorators.cache import cache_control
# from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from rstr.config import Config
import logging

# @vary_on_header s('Cookie')
# @cache_control(private=True, must_revalidate=True, max_age=3600)
# @never_cache
@vary_on_cookie
def index(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    # request.session.clear()
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session.session_key).getSessionData()
        request.session = data

    login = render_to_string('rstr/login.html', {'session' : request.session}, context_instance=RequestContext(request))
    leftCol = render_to_string('rstr/left.html', {'blocks' : [login]})
    centerCol = render_to_string('rstr/center.html', {})
    rightCol = render_to_string('rstr/right.html', {})
    return render_to_response('rstr/index.html', {'logged' : request.session.get('logged', False),
                                                  'copy' : '&copy; Pablo Alvarez de Sotomayor Posadillo',
                                                  'session' : request.session,
                                                  'leftCol' : leftCol,
                                                  'centerCol' : centerCol,
                                                  'rightCol' : rightCol})

# def error(request):
    # p = get_object_or_404(Poll, pk=poll_id)

def auth_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponse("You're logged in.")
            else:
                # Return a 'disabled account' error message
                return HttpResponse("Your account is disabled.")
        else:
            # Return an 'invalid login' error message.
            return HttpResponse("Username or password error.")
    elif request.method == 'GET':
        return HttpResponse("Login.")
    else:
        raise Http404

def auth_logout(request):
    logout(request)
    return HttpResponse("You're logged out.")
