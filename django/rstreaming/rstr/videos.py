# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

import os
import logging
import subprocess
from datetime import datetime

from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template import RequestContext
from django.template.loader import render_to_string

from rstr.user import LoginForm
from rstr.config import Config
from rstr.common import ErrorClear
from rstr.models import streaming
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

        centerBlocks = []
        try:
            videoStr = streaming.objects.all()
            for video in videoStr:
                centerBlocks = [render_to_string('rstr/section.html', {'title' : 'login', 'content': str(video.idStreaming)})]
        except streaming.DoesNotExist:
            pass
        self.render = MainViewer(request).render(leftBlocks, [], [])

    def getRender(self):
        return self.render

class StrForm(forms.Form):
    isVideo = forms.BooleanField(label='Emitir Video',
                                 required=False)
    srcIP = forms.IPAddressField(label='Ip de origen',
                                 required=False)
    srcPort = forms.IntegerField(label='Puerto de origen',
                                 required=False)
    srcMux = forms.ChoiceField(label='Multiplexor de origen',
                                choices=[('ogg', 'ogg'), ('ffmpeg{mux=flv}', 'mp4'), ('webm', 'webm')],
                                 required=False)
    vStream = forms.ChoiceField(label='Video a emitir',
                                choices=[],
                                required=True)

class StreamView():
    def __init__(self, request):
        logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
        messages.set_level(request, messages.INFO)
        if request.session.get('isConfig', False) is False:
            request.session.set_expiry(600)
            data = Config(request.session).getSessionData()
            request.session.update(data)
            request.session['isConfig'] = True
        if request.method == 'GET':
            form = StrForm(error_class=ErrorClear)
            form.fields['isVideo'].initial = False
            form.fields['srcIP'].initial = request.META['REMOTE_ADDR']
            form.fields['srcPort'].initial = 9000
            form.fields['vStream'].choices = self.userVideos(request)
            self.render = MainViewer(request).render([], [render_to_string('rstr/form.html', {'form' : form, 'action' : request.session['base_url'] + '/stream', 'id' : 'stream'}, context_instance=RequestContext(request))], [])
        elif request.method == 'POST':
            form = StrForm(request.POST, error_class=ErrorClear)
            form.fields['isVideo'].initial = False
            form.fields['srcIP'].initial = request.META['REMOTE_ADDR']
            form.fields['srcPort'].initial = 9000
            form.fields['vStream'].choices = self.userVideos(request)

            if form.is_valid():
                try:
                    v = video.objects.filter(idVideo=form.cleaned_data['vStream'])[0]
                except video.DoesNotExist:
                    v = None
                if form.cleaned_data['isVideo'] is True and v is not None:
                    clvc = None
                    if v.format == 'video/mp4':
                        cvlc = subprocess.Popen(["/usr/bin/cvlc " + v.path + " --sout '#http{mux=ffmpeg{mux=flv},dst=" + request.session['strIP'] + ":" + request.session['strPort'] + "/} -no-sout-rtp-sap -no-sout-standard-sap -sout-keep' --ttl 12"],
                                                shell=True)
                    elif v.format == 'video/webm':
                        cvlc = subprocess.Popen(["/usr/bin/cvlc " + v.path + " --sout '#http{mux=webm,dst=" + request.session['strIP'] + ":" + request.session['strPort'] + "/} -no-sout-rtp-sap -no-sout-standard-sap -sout-keep' --ttl 12"],
                                                shell=True)
                    elif v.format == 'video/ogg':
                        cvlc = subprocess.Popen(["/usr/bin/cvlc " + v.path + " --sout '#http{mux=ogg,dst=" + request.session['strIP'] + ":" + request.session['strPort'] + "/} -no-sout-rtp-sap -no-sout-standard-sap -sout-keep' --ttl 12"],
                                                shell=True)
                    else:
                        messages.add_message(request, messages.ERROR, 'Video type not supported')

                    if clvc is not None:
                        vStream = streaming(src=form.cleaned_data['srcIP'], port=form.cleaned_data['srcPort'], mux=form.cleaned_data['srcMux'], vMode=form.cleaned_data['isVideo'], pid=cvlc.pid,video=v, owner=request.session['user'])
                        vStream.save()
                        messages.add_message(request, messages.INFO, 'Video streaming')
                elif form.cleaned_data['isVideo'] is False:
                    if form.cleaned_data['srcMux'] != "ffmpeg{mux=flv}" and form.cleaned_data['srcMux'] != "webm" and form.cleaned_data['srcMux'] != "ogg":
                        messages.add_message(request, messages.ERROR, 'Video type not supported')
                    else:
                        cvlc = subprocess.Popen(["/usr/bin/cvlc http://" + str(form.cleaned_data['srcIP']) + ":" + str(form.cleaned_data['srcPort']) + " --sout '#http{mux=" + str(form.cleaned_data['srcMux']) + ",dst=" + request.session['strIP'] + ":" + request.session['strPort'] + "/} -no-sout-rtp-sap -no-sout-standard-sap -sout-keep' --ttl 12"],
                                                shell=True)
                        vStream = streaming(src=form.cleaned_data['srcIP'], port=form.cleaned_data['srcPort'], mux=form.cleaned_data['srcMux'], vMode=form.cleaned_data['isVideo'], pid=cvlc.pid,video=v, owner=request.session['user'])
                        vStream.save()
                        messages.add_message(request, messages.ERROR, 'External video streaming.')
                else:
                    messages.add_message(request, messages.ERROR, 'If you select the video mode you must select a video.')
                # os.waitpid(p.pid, 0)[1]
                self.render = HttpResponseRedirect('/streaming')
            else:
                for error in form.errors:
                    messages.add_message(request, messages.ERROR, 'Error en ' + error + ': ' + str(form._errors[error]))
                if request.META.get('HTTP_REFERER', False) is not False:
                    self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
                else:
                    self.render = HttpResponseRedirect('/index')
        else:
            raise Http404

    def userVideos(self, request):
        init = []
        try:
            videos = video.objects.filter(owner=request.session['user'])
            for v in videos:
                init.append((v.idVideo, v.name))
        except video.DoesNotExist:
            pass
        return init

    def getRender(self):
        return self.render

class VideosView():
    LIST = 0
    VIEW = 1
    DELETE = 2
    def __init__(self, request, action=0, key=None):
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
        else:
            try:
                myVideos = video.objects.filter(owner = request.session['user'])
                leftBlocks = [render_to_string('rstr/section.html', {'title' : 'Mis vídeos', 'content' : render_to_string('rstr/myVideo.html', {'videos' : myVideos, 'session' : request.session}).encode('utf-8')})]
            except video.DoesNotExist:
                pass

        centerBlocks = []
        if action == self.LIST:
            try:
                videoList = video.objects.all()
                centerBlocks = [render_to_string('rstr/section.html', {'title' : 'Lista de videos', 'content': render_to_string('rstr/videoList.html', {'videos' : videoList, 'session' : request.session}).encode('utf-8')})]
            except video.DoesNotExist:
                pass
        elif action == self.VIEW:
            if key is not None:
                try:
                    v = video.objects.get(idVideo=key)
                    media = request.session['base_url'] + '/media/'
                    bfile = media + v.path[v.path.rfind('/')+1:v.path.rfind('.')]
                    src = {'ogv' : bfile + '.ogv', 'mp4' : bfile + '.mp4', 'webm' : bfile + '.webm', 'flash' : request.session['base_url'] + '/static/flowplayer/flowplayer-3.2.5.swf'}
                    centerBlocks = [render_to_string('rstr/section.html', {'title' : v.name, 'content': render_to_string('rstr/video.html', {'controls' : True, 'src' : src})})]
                except video.DoesNotExist:
                    pass
        elif action == self.DELETE:
                try:
                    v = video.objects.get(idVideo=key, owner=request.session['user'])
                    name = v.name
                    os.remove(v.path)
                    v.delete()
                    centerBlocks = ['<p>Video ' + name + ' deleted.</p>']
                except video.DoesNotExist:
                    pass

        # Ultimos subidos, ultimos usuarios que han subido, usuarios que mas han subido, ...
        rightBlocks = []

        self.render = MainViewer(request).render(leftBlocks, centerBlocks, rightBlocks)

    def getRender(self):
        return self.render

class UploadForm(forms.Form):
    title = forms.CharField(label='Título',
                               min_length=5,
                               max_length=80,
                               required=True)
    description = forms.CharField(label='Descripción',
                                  min_length=5,
                                  max_length=250,
                                  required=True)
    fileUpload = forms.FileField(label='Fichero',
                                 required=True)

class UploadView():
    def __init__(self, request):
        logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
        messages.set_level(request, messages.INFO)
        if request.session.get('isConfig', False) is False:
            request.session.set_expiry(600)
            data = Config(request.session).getSessionData()
            request.session.update(data)
            request.session['isConfig'] = True
        if request.method == 'GET':
            leftBlocks = [self.getMyVideos(request.session)]
            centerBlocks = [self.getUploadVideo(request.session['base_url'], request)]
            self.render = MainViewer(request).render(leftBlocks, centerBlocks, [])
        elif request.method == 'POST':
            form = UploadForm(request.POST, request.FILES, error_class=ErrorClear)
            if form.is_valid():
                upFile = request.FILES['fileUpload']
                if upFile.size > 0:
                    path = ''
                    if request.session.get('upload_path', False):
                        path = request.session['upload_path']+'/'
                    path += upFile.name
                    destination = open(path, 'wb+')
                    for chunk in upFile.chunks():
                        destination.write(chunk)
                    destination.close()
                    v = video(name=form.cleaned_data['title'], description=form.cleaned_data['description'], path=path, format=upFile.content_type, pub_date=datetime.now(), owner=request.session['user'])
                    v.save()
            else:
                for error in form.errors:
                    messages.add_message(request, messages.ERROR, 'Error en ' + error + ': ' + str(form._errors[error]))
            if request.META.get('HTTP_REFERER', False) is not False:
                self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                self.render = HttpResponseRedirect('/index')            
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

    def getUploadVideo(self, base_url, request):
        content = render_to_string('rstr/form.html', {'form' : UploadForm(request.POST, request.FILES, error_class=ErrorClear), 'action' : base_url + '/upload', 'upload' : True}, context_instance=RequestContext(request))
        return render_to_string('rstr/section.html', {'title' : 'Subir vídeo', 'content' : content})

    def getRender(self):
        return self.render
