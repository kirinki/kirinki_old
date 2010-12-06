# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

import logging
from django import forms
from django.core import validators
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.template import RequestContext
from django.core.mail import send_mail
from recaptcha.client import captcha
from django.forms.util import ErrorList
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from rstr.config import Config
from rstr.mainviewer import MainViewer

class ErrorClear(ErrorList):
    def __str__(self):
        return self.as_clear().encode('utf-8')
    def as_clear(self):
        if not self:
            return ''
        return ''.join(['%s' % e for e in self])

class LoginForm(forms.Form):
    username = forms.CharField(label='username',
                               min_length=3,
                               max_length=30,
                               required=True,
                               error_messages={'invalid': 'The username must have between 3 and 30 characters.'})
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput,
                               min_length=5,
                               max_length=60,
                               required=True,
                               error_messages={'invalid': 'The password must have between 5 and 60 characters.'})

class LoginView():
    def __init__(self, request):
        form = LoginForm(request.POST, error_class=ErrorClear)
        if request.method == 'POST':
            logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
            logging.debug('Login POST')
            if request.session['user'].is_authenticated():
                messages.add_message(request, messages.ERROR, 'User already logged in')
                if request.META.get('HTTP_REFERER', False) is not False:
                    self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
                else:
                    self.render = HttpResponseRedirect('/rstr/index')
            if form.is_valid():
                logging.debug('Login POST Valid')
                logging.debug(form.cleaned_data['username']+' '+form.cleaned_data['password'])
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        messages.add_message(request, messages.INFO, 'User logged in')
                        request.session['user'] = user
                        if request.META.get('HTTP_REFERER', False) is not False:
                            self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
                        else:
                            self.render = HttpResponseRedirect('/rstr/index')
                    else:
                        # Return a 'disabled account' error message
                        messages.add_message(request, messages.ERROR, 'Your account is disabled.')
                        if request.META.get('HTTP_REFERER', False) is not False:
                            self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
                        else:
                            self.render = HttpResponseRedirect('/rstr/index')
                else:
                    # Return an 'invalid login' error message.
                    messages.add_message(request, messages.ERROR, 'Username or password error.')
                    if request.META.get('HTTP_REFERER', False) is not False:
                        self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
                    else:
                        self.render = HttpResponseRedirect('/rstr/index')
            else:
                for error in form.errors:
                    messages.add_message(request, messages.ERROR, 'Error en ' + error + ': ' + str(form._errors[error]))
                if request.META.get('HTTP_REFERER', False) is not False:
                    self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
                else:
                    self.render = HttpResponseRedirect('/rstr/index')            
        elif request.method == 'GET':
            logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
            messages.set_level(request, messages.INFO)
            if request.session.get('isConfig', False) is False:
                request.session.set_expiry(600)
                data = Config(request.session).getSessionData()
                request.session.update(data)
                request.session['isConfig'] = True
            centerBlocks = []
            if not request.session['user'].is_authenticated():
                centerBlocks = [render_to_string('rstr/section.html', {'title' : 'Login', 'content': render_to_string('rstr/form.html', {'form' : form, 'action' : request.session['base_url']+'/login'}, context_instance=RequestContext(request))})]
            self.render = MainViewer(request).render([],centerBlocks,[])
        else:
            raise Http404

    def getRender(self):
        return self.render

class RegisterForm(forms.Form):
    username = forms.CharField(label='username',
                               min_length=3,
                               max_length=30,
                               required=False)
    fname = forms.CharField(label='first name',
                            min_length=3,
                            max_length=30,
                            required=False)
    lname = forms.CharField(label='last name',
                            min_length=3,
                            max_length=30,
                            required=False)
    email = forms.CharField(label='email',
                            min_length=3,
                            max_length=30,
                            required=False)
    password = forms.CharField(label='password',
                            widget=forms.PasswordInput,
                            min_length=5,
                            max_length=60,
                            required=False)
    rpassword = forms.CharField(label='repeat password',
                                widget=forms.PasswordInput,
                                min_length=5,
                                max_length=60,
                                required=False)

class RegisterView():
    def __init__(self, request):
        logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
        if request.method == 'GET':
            if request.session.get('isConfig', False) is False:
                messages.set_level(request, messages.INFO)
                request.session.set_expiry(600)
                data = Config(request.session).getSessionData()
                request.session.update(data)
                request.session['isConfig'] = True
            centerBlocks = []
            if not request.session['user'].is_authenticated():
                centerBlocks = [render_to_string('rstr/section.html', {'title' : 'Register', 'content': render_to_string('rstr/register.html', {'session' : request.session, 'captcha' : captcha.displayhtml('6LefRr8SAAAAAMncFelaGsop60Uuon0MCL6H-aP3')}, context_instance=RequestContext(request))})]
            self.render = MainViewer(request).render([],centerBlocks,[])
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
                    request.session.set_expiry(600)
                    data = Config(request.session).getSessionData()
                    request.session.update(data)
                    request.session['isConfig'] = True
                if request.META.get('HTTP_REFERER', False) is not False:
                    self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
                else:
                    self.render = HttpResponseRedirect('/rstr/index')
        else:
            raise Http404

    def getRender(self):
        return self.render
