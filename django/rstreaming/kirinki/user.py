# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

# Python general imports
import hashlib
import random
from datetime import datetime, timedelta

# Django imports
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.mail import send_mail
from recaptcha.client import captcha
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Application imports
from kirinki.config import Config
from kirinki.common import ErrorClear
from kirinki.log import Log
from kirinki.mainviewer import MainViewer
from kirinki.message import Message
from kirinki.models import UserProfile

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

class LoginController():
    '''Class that implements the Login controller'''
    
    def __init__(self, request):
        if request.session.get('isConfig', False) is False:
            Config.getSession(request.session)

        form = LoginForm(request.POST, error_class=ErrorClear)
        if request.method == 'GET':
            # GET request
            centerBlocks = []
            if not request.session['user'].is_authenticated():
                centerBlocks = [render_to_string('kirinki/section.html', {'title' : 'Login', 'content': render_to_string('kirinki/form.html', {'form' : form, 'action' : request.session['base_url']+'/login'}, context_instance=RequestContext(request))})]
            self.render = MainViewer(request).render([],centerBlocks,[])
            
        elif request.method == 'POST':
            # POST request
            Log.debug('Login POST')

            if request.session['user'].is_authenticated():
                Message.pushMessage(request, Message.ERROR, 'User already logged in')
            if form.is_valid():
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        Message.pushMessage(request, Message.INFO, 'User logged in')
                        request.session['user'] = user
                    else:
                        # Return a 'disabled account' error message
                        Message.pushMessage(request, Message.ERROR, 'Your account is disabled.')
                else:
                    # Return an 'invalid login' error message.
                    Message.pushMessage(request, Message.ERROR, 'Username or password error.')
            else:
                for error in form.errors:
                    Message.pushMessage(request, Message.ERROR, 'Error en ' + error + ': ' + str(form._errors[error]))

            # The return page is the same for all the situations of this request.
            if request.META.get('HTTP_REFERER', False) is not False:
                self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                self.render = HttpResponseRedirect('/index')
                
        else:
            # If there's not GET neither POST request there's an error
            raise Http404
                
    def getRender(self):
        '''This method return the html generated page'''
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

class RegisterController():
    '''Class that implements the Register controller'''

    def __init__(self, request):
        if request.session.get('isConfig', False) is False:
            Config.getSession(request.session)

        form = RegisterForm(request.POST, error_class=ErrorClear)
        if request.method == 'GET':
            # GET request
            centerBlocks = []
            if not request.session['user'].is_authenticated():
                centerBlocks = [render_to_string('kirinki/section.html',
                                                 {'title' : 'Register',
                                                  'content': render_to_string('kirinki/form.html', {'form' : form, 'action' : request.session['base_url']+'/register', 'captcha' : captcha.displayhtml('6LefRr8SAAAAAMncFelaGsop60Uuon0MCL6H-aP3')},
                                                                              context_instance=RequestContext(request))})]
            self.render = MainViewer(request).render([],centerBlocks,[])
            
        elif request.method == 'POST':
            # POST request
            if form.is_valid():
                Log.debug('Form valid')
                if form.cleaned_data['password'] != form.cleaned_data['rpassword']:
                    Log.debug('Passwords doesn\'t match')
                    Message.pushMessage(request, Message.INFO, 'Passwords doesn\'t match.')
                else:
                    Log.debug('Passwords match')
                    remote_ip = request.META['REMOTE_ADDR']
                    challenge = request.REQUEST.get('recaptcha_challenge_field')
                    response = request.REQUEST.get('recaptcha_response_field')
                    recaptcha_response = captcha.submit(challenge, response, '6LefRr8SAAAAAPpY8WNoxo19nh0Rre5BCB9JfLJV', remote_ip)

                    if recaptcha_response.is_valid:
                        Log.debug('Recaptcha is valid')
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
                                      'no-reply@kirinki.net',
                                      [user.email.encode('utf-8')],
                                      fail_silently=False)

                            Message.pushMessage(request, Message.INFO, 'User registered. To activate the account please visit the url inicated in your email.')
                    else:
                        Log.debug('Recaptcha is not valid')
                        Message.pushMessage(request, Message.ERROR, 'User not registered. ' + recaptcha_response.error_code)
            else:
                Log.debug('Form is not valid')
                for error in form.errors:
                    Message.pushMessage(request, Message.ERROR, 'Error en ' + error + ': ' + str(form._errors[error]))

            if request.META.get('HTTP_REFERER', False) is not False:
                self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                self.render = HttpResponseRedirect('/index')
        else:
            raise Http404

    def getRender(self):
        '''This method returns the html page generated.'''
        return self.render

class LogoutController():
    '''Class that implements the Logout controller'''
    
    def __init__(self, request):
        if request.session.get('isConfig', False) is False:
            Config.getSession(request.session)

        if request.session['user'].is_authenticated():
            logout(request)
            Message.pushMessage(request, Message.INFO, 'User logged out.')
        else:
            Message.pushMessage(request, Message.ERROR, 'User not logged in.')
            
        if request.META.get('HTTP_REFERER', False) is not False:
            self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            self.render = HttpResponse('/logout')

    def getRender(self):
        return self.render

class ActivationController():
    '''Class that implements the User Activation controller'''

    def __init__(self, request, key):
        try:
            Log.debug(key)
            up = UserProfile.objects.get(activation_key=key)
            if up.key_expires < datetime.today():
                Message.pushMessage(request, Message.INFO, 'The activation key has expired.')
            else:
                user = up.user
                user.is_active = True
                user.save()
                Message.pushMessage(request, Message.INFO, 'User ' + user.username + ' is activated')
                up.delete()
        except UserProfile.DoesNotExist:
            Message.pushMessage(request, Message.INFO, 'User Profile does not exists')
        self.render = HttpResponseRedirect('/index')

    def getRender(self):
        return self.render

    def cleanProfiles():
        profiles = UserProfile.objects.all(key_expires < datetime.today())
        for profile in profiles:
            profile.delete()

class AdminController():
    '''Class that implements the Administration Panel controller'''
    
    def __init__(self, request):
        if request.session.get('isConfig', False) is False:
            Config.getSession(request.session)
        self.render = MainViewer(request).render([],[],[])

    def getRender(self):
        return self.render

class AccountController():
    '''Class that implements the User Panel controller'''

    def __init__(self, request):
        if request.session.get('isConfig', False) is False:
            Config.getSession(request.session)
        self.render = MainViewer(request).render([],[],[])

    def getRender(self):
        return self.render
