# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

import logging
from datetime import datetime

from django import forms
from django.contrib import messages
from django.template import RequestContext
from django.template.loader import render_to_string

from rstr.user import LoginForm
from rstr.config import Config
from rstr.common import ErrorClear
from rstr.models import video
from rstr.mainviewer import MainViewer

class StreamingView():
    def __init__(self, request):
        logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
        messages.set_level(request, messages.INFO)
        if request.session.get('isConfig', False) is False:
            request.session.set_expiry(600)
            data = Config(request.session).getSessionData()
            request.session.update(data)
            request.session['isConfig'] = True
        leftBlocks = []
        if not request.session['user'].is_authenticated():
            leftBlocks = [render_to_string('rstr/section.html', {'title' : 'login', 'content': render_to_string('rstr/form.html', {'form' : LoginForm(), 'action' : request.session['base_url'] + '/login'}, context_instance=RequestContext(request))})]
        self.render = MainViewer(request).render(leftBlocks, [], [])

    def getRender(self):
        return self.render

class VideosView():
    def __init__(self, request):
        logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
        messages.set_level(request, messages.INFO)
        if request.session.get('isConfig', False) is False:
            request.session.set_expiry(600)
            data = Config(request.session).getSessionData()
            request.session.update(data)
            request.session['isConfig'] = True
        leftBlocks = []
        if not request.session['user'].is_authenticated():
            leftBlocks = [render_to_string('rstr/section.html', {'title' : 'login', 'content': render_to_string('rstr/form.html', {'form' : LoginForm(), 'action' : request.session['base_url']+'/login'}, context_instance=RequestContext(request))})]
        self.render = MainViewer(request).render(leftBlocks, [], [])

    def getRender(self):
        return self.render

class StreamView():
    def __init__(self, request):
        logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
        messages.set_level(request, messages.INFO)
        if request.session.get('isConfig', False) is False:
            request.session.set_expiry(600)
            data = Config(request.session).getSessionData()
            request.session.update(data)
            request.session['isConfig'] = True
        self.render = MainViewer(request).render([], [], [])

    def getRender(self):
        return self.render

class UploadForm(forms.Form):
    title = forms.CharField(label='Título',
                               min_length=5,
                               max_length=80,
                               required=True)
    description = forms.CharField(label='Descripción:',
                                  min_length=5,
                                  max_length=250,
                                  required=True)
    fileUpload = forms.FileField(label='Fichero:',
                                 required=True)

class UploadView():
    def __init__(self, request):
        if request.method == 'GET':
            logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
            messages.set_level(request, messages.INFO)
            if request.session.get('isConfig', False) is False:
                request.session.set_expiry(600)
                data = Config(request.session).getSessionData()
                request.session.update(data)
                request.session['isConfig'] = True
            leftBlocks = [self.getMyVideos(request.session)]
            centerBlocks = [self.getUploadVideo(request.session['base_url'])]
            self.render = MainViewer(request).render(leftBlocks, centerBlocks, [])
        elif request.method == 'POST':
            form = UploadForm(request.POST, error_class=ErrorClear)
            if form.is_valid():
                upFile = request.FILES['fileUpload']
                if upFile.size > 0:
                    path = ''
                    if request.session.get('upload', False):
                        path = request.session['upload']+'/'
                    path += upFile.name
                    destination = open(path, 'wb+')
                    for chunk in upFile.chunks():
                        destination.write(chunk)
                    destination.close()
                    v = video(name=form.cleaned_data['name'], description=form.cleaned_data['description'], path=path, format=upFile.content_type, pub_date=datetime.now(), owner=request.session['user'])
            else:
                for error in form.errors:
                    messages.add_message(request, messages.ERROR, 'Error en ' + error + ': ' + str(form._errors[error]))
                if request.META.get('HTTP_REFERER', False) is not False:
                    self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
                else:
                    self.render = HttpResponseRedirect('/rstr/index')            
        else:
            raise Http404

    def getMyVideos(self, session):
        content = ''
        try:
            myVideos = video.objects.filter(owner = session['user'])
            content = render_to_string('rstr/myVideo.html', {'videos' : myVideos, 'session' : session}).encode('utf-8')
        except video.DoesNotExist:
            pass
        return render_to_string('rstr/section.html', {'title' : 'Mis vídeos', 'content' : content})

    def getUploadVideo(self, base_url):
        content = render_to_string('rstr/form.html', {'form' : UploadForm(), 'action' : base_url + '/upload'})
        return render_to_string('rstr/section.html', {'title' : 'Subir vídeo', 'content' : content})

    def getRender(self):
        return self.render
