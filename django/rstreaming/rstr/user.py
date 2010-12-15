# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

import sha
import random
import logging
from datetime import datetime, timedelta

from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template import RequestContext
from django.core.mail import send_mail
from recaptcha.client import captcha
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from rstr.config import Config
from rstr.common import ErrorClear
from rstr.mainviewer import MainViewer
from rstr.models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(label='username',
                               min_length=3,
                               max_length=30,
                               required=True)
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput,
                               min_length=5,
                               max_length=60,
                               required=True)

class LoginView():
    def __init__(self, request):
        form = LoginForm(request.POST, error_class=ErrorClear)
        logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
        messages.set_level(request, messages.INFO)
        if request.session.get('isConfig', False) is False:
            request.session.set_expiry(600)
            data = Config(request.session).getSessionData()
            request.session.update(data)
            request.session['isConfig'] = True
        if request.method == 'GET':
            centerBlocks = []
            if not request.session['user'].is_authenticated():
                centerBlocks = [render_to_string('rstr/section.html', {'title' : 'Login', 'content': render_to_string('rstr/form.html', {'form' : form, 'action' : request.session['base_url']+'/login'}, context_instance=RequestContext(request))})]
            self.render = MainViewer(request).render([],centerBlocks,[])
        elif request.method == 'POST':
            logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
            logging.debug('Login POST')
            if request.session['user'].is_authenticated():
                messages.add_message(request, messages.ERROR, 'User already logged in')
                if request.META.get('HTTP_REFERER', False) is not False:
                    self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
                else:
                    self.render = HttpResponseRedirect('/index')
            if form.is_valid():
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        messages.add_message(request, messages.INFO, 'User logged in')
                        request.session['user'] = user
                        if request.META.get('HTTP_REFERER', False) is not False:
                            self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
                        else:
                            self.render = HttpResponseRedirect('/index')
                    else:
                        # Return a 'disabled account' error message
                        messages.add_message(request, messages.ERROR, 'Your account is disabled.')
                        if request.META.get('HTTP_REFERER', False) is not False:
                            self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
                        else:
                            self.render = HttpResponseRedirect('/index')
                else:
                    # Return an 'invalid login' error message.
                    messages.add_message(request, messages.ERROR, 'Username or password error.')
                    if request.META.get('HTTP_REFERER', False) is not False:
                        self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
                    else:
                        self.render = HttpResponseRedirect('/index')
            else:
                for error in form.errors:
                    messages.add_message(request, messages.ERROR, 'Error en ' + error + ': ' + str(form._errors[error]))
                if request.META.get('HTTP_REFERER', False) is not False:
                    self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
                else:
                    self.render = HttpResponseRedirect('/index')            
        else:
            raise Http404

    def getRender(self):
        return self.render

class RegisterForm(forms.Form):
    username = forms.CharField(label='username',
                               min_length=3,
                               max_length=30,
                               required=True)
    first_name = forms.CharField(label='first name',
                                 min_length=3,
                                 max_length=30,
                                 required=False)
    last_name = forms.CharField(label='last name',
                                min_length=3,
                                max_length=30,
                                required=False)
    email = forms.EmailField(label='email',
                             min_length=6,
                             max_length=50,
                             required=False)
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput,
                               min_length=5,
                               max_length=60,
                               required=True)
    rpassword = forms.CharField(label='repeat password',
                                widget=forms.PasswordInput,
                                min_length=5,
                                max_length=60,
                                required=True)

class RegisterView():
    def __init__(self, request):
        logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
        form = RegisterForm(request.POST, error_class=ErrorClear)
        if request.session.get('isConfig', False) is False:
            messages.set_level(request, messages.INFO)
            request.session.set_expiry(600)
            data = Config(request.session).getSessionData()
            request.session.update(data)
            request.session['isConfig'] = True
        if request.method == 'GET':
            centerBlocks = []
            if not request.session['user'].is_authenticated():
                centerBlocks = [render_to_string('rstr/section.html',
                                                 {'title' : 'Register',
                                                  'content': render_to_string('rstr/form.html', {'form' : form, 'action' : request.session['base_url']+'/register', 'captcha' : captcha.displayhtml('6LefRr8SAAAAAMncFelaGsop60Uuon0MCL6H-aP3')},
                                                                              context_instance=RequestContext(request))})]
            self.render = MainViewer(request).render([],centerBlocks,[])
        elif request.method == 'POST':
            if form.is_valid():
                logging.debug('Form valid')
                if form.cleaned_data['password'] != form.cleaned_data['rpassword']:
                    logging.debug('Passwords doesn\'t match')
                    messages.add_message(request, messages.INFO, 'Passwords doesn\'t match.')
                else:
                    logging.debug('Passwords match')
                    remote_ip = request.META['REMOTE_ADDR']
                    challenge = request.REQUEST.get('recaptcha_challenge_field')
                    response = request.REQUEST.get('recaptcha_response_field')
                    recaptcha_response = captcha.submit(challenge, response, '6LefRr8SAAAAAPpY8WNoxo19nh0Rre5BCB9JfLJV', remote_ip)

                    if recaptcha_response.is_valid:
                        logging.debug('Recaptcha is valid')
                        try:
                            User.objects.get(username=form.cleaned_data['username'])
                        except User.DoesNotExist:
                            user = User.objects.create_user(request.POST['username'], form.cleaned_data['email'], form.cleaned_data['password'])
                            user.is_active = False
                            user.first_name = form.cleaned_data['first_name']
                            user.last_name = form.cleaned_data['last_name']
                            user.groups.add(Group.objects.get(name='users'))
                            user.save()

                            salt = sha.new(str(random.random())).hexdigest()[:5]
                            activation_key = sha.new(salt+user.username).hexdigest()
                            key_expires = datetime.today() + timedelta(2)
                            
                            new_profile = UserProfile(user=user,
                                                      activation_key=activation_key,
                                                      key_expires=key_expires)
                            new_profile.save()
                            
                            email_subject = 'Ritho\'s Streaming account confirmation'
                            email_body = "Hello, %s, and thanks for signing up for an rstreaming account!\n\nTo activate your account, click this link within 48 hours:\n\n%s/account/confirm/%s" % (user.username, request.session['base_url'], new_profile.activation_key)
                            send_mail(email_subject,
                                      email_body,
                                      'rstr@ritho.net',
                                      [user.email.encode('utf-8')],
                                      fail_silently=False)

                            messages.add_message(request, messages.INFO, 'User registered. To activate the account please visit the url inicated in your email.')
                    else:
                        logging.debug('Recaptcha is not valid')
                        messages.add_message(request, messages.ERROR, 'User not registered. ' + recaptcha_response.error_code)
            else:
                logging.debug('Form is not valid')
                for error in form.errors:
                    messages.add_message(request, messages.ERROR, 'Error en ' + error + ': ' + str(form._errors[error]))

            if request.META.get('HTTP_REFERER', False) is not False:
                self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                self.render = HttpResponseRedirect('/index')
        else:
            raise Http404

    def getRender(self):
        return self.render

class LogoutView():
    def __init__(self, request):
        if request.session.get('isConfig', False) is False:
            request.session.set_expiry(600)
            data = Config(request.session).getSessionData()
            request.session.update(data)
            request.session['isConfig'] = True
        if request.session['user'].is_authenticated():
            logout(request)
            messages.add_message(request, messages.INFO, 'User logged out.')
            if request.META.get('HTTP_REFERER', False) is not False:
                self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                self.render = HttpResponseRedirect('/index')
        else:
            messages.add_message(request, messages.ERROR, 'User not logged in.')
            if request.META.get('HTTP_REFERER', False) is not False:
                self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                self.render = HttpResponse('/logout')

    def getRender(self):
        return self.render

class ActivationView():
    def __init__(self, request, key):
        logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
        try:
            logging.debug(key)
            up = UserProfile.objects.get(activation_key=key)
            if up.key_expires < datetime.today():
                messages.add_message(request, messages.INFO, 'The activation key has expired.')
            else:
                user = up.user
                user.is_active = True
                user.save()
                messages.add_message(request, messages.INFO, 'User ' + user.username + ' is activated')
                up.delete()
        except UserProfile.DoesNotExist:
            messages.add_message(request, messages.INFO, 'User Profile does not exists')
        self.render = HttpResponseRedirect('/index')

    def getRender(self):
        return self.render

    def cleanProfiles():
        profiles = UserProfile.objects.all(key_expires < datetime.today())
        for profile in profiles:
            profile.delete()

class AdminView():
    def __init__(self, request):
        logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
        messages.set_level(request, messages.INFO)
        if request.session.get('isConfig', False) is False:
            request.session.set_expiry(600)
            data = Config(request.session).getSessionData()
            request.session.update(data)
            request.session['isConfig'] = True
        self.render = MainViewer(request).render([],[],[])

    def getRender(self):
        return self.render

class AccountView():
    def __init__(self, request):
        logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
        messages.set_level(request, messages.INFO)
        if request.session.get('isConfig', False) is False:
            request.session.set_expiry(600)
            data = Config(request.session).getSessionData()
            request.session.update(data)
            request.session['isConfig'] = True
        self.render = MainViewer(request).render([],[],[])

    def getRender(self):
        return self.render
