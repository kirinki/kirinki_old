from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.views.decorators.vary import vary_on_headers
from django.views.decorators.vary import vary_on_cookie
# from django.views.decorators.cache import cache_control
# from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from rstr.config import Config
import logging

# @vary_on_header s('Cookie')
# @cache_control(private=True, must_revalidate=True, max_age=3600)
# @never_cache
@vary_on_cookie
def index(request):
    logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
    request.session.clear()
    if request.session.get('isConfig', False) is False:
        request.session.set_expiry(600)
        data = Config(request.session.session_key).getSessionData()
        request.session = data

    leftCol = render_to_string('rstr/left.html', {})
    centerCol = render_to_string('rstr/center.html', {})
    rightCol = render_to_string('rstr/right.html', {})
    return render_to_response('rstr/index.html', {'logged' : request.session.get('logged', False),
                                                  'copy' : '&copy; Pablo Alvarez de Sotomayor Posadillo',
                                                  'session' : request.session,
                                                  'leftCol' : leftCol,
                                                  'centerCol' : centerCol,
                                                  'rightCol' : rightCol})

def error(request):
    #  if request.method == 'POST':
    # p = get_object_or_404(Poll, pk=poll_id)
    raise Http404

def login(request):
    m = Member.objects.get(username=request.POST['username'])
    if m.password == request.POST['password']:
        request.session['member_id'] = m.id
        return HttpResponse("You're logged in.")
    else:
        return HttpResponse("Your username and password didn't match.")

def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")
