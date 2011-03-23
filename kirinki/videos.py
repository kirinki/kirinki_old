# -*- coding: utf-8 -*-
__license__ = "GNU Affero General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

# This file is part of Kirinki.
# 
# Kirinki is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as 
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# Kirinki is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public
# License along with kirinki. If not, see <http://www.gnu.org/licenses/>.

# Python general imports
import os
import os.path
import subprocess
import httplib
from datetime import datetime

# Django imports
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string

# Application imports
from kirinki.config import Config
from kirinki.common import ErrorClear
from kirinki.mainviewer import MainViewer
from kirinki.models import streaming
from kirinki.models import video
from kirinki.message import Message
from kirinki.user import LoginForm

class StreamingController():
    '''Class that implements the Streaming controller'''
    def __init__(self, request):
        if request.session.get('isConfig', False) is False:
            Config.getSession(request.session)

        # Left block
        leftBlocks = []
        if not request.session['user'].is_authenticated():
            leftBlocks = [render_to_string('kirinki/section.html', {'title' : 'login', 'content': render_to_string('kirinki/form.html', {'form' : LoginForm(), 'action' : request.session['base_url'] + '/login'}, context_instance=RequestContext(request))})]

        # Center block
        centerBlocks = []
        try:
            videoStr = streaming.objects.all()
            for video in videoStr:
                centerBlocks = [render_to_string('kirinki/section.html', {'title' : 'login', 'content': str(video.idStreaming)})]
        except streaming.DoesNotExist:
            pass
        
        self.render = MainViewer(request).render(leftBlocks, centerBlocks, [])

    def getRender(self):
        '''This method return the html rendered'''
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

class StreamController():
    '''Class to implement the Stream controller'''
    
    def __init__(self, request):
        if request.session.get('isConfig', False) is False:
            Config.getSession(request.session)

        if request.method == 'GET':
            # GET request
            form = StrForm(error_class=ErrorClear)
            form.fields['isVideo'].initial = False
            form.fields['srcIP'].initial = request.META['REMOTE_ADDR']
            form.fields['srcPort'].initial = 9000
            form.fields['vStream'].choices = self.userVideos(request)
            self.render = MainViewer(request).render([], [render_to_string('kirinki/form.html', {'form' : form, 'action' : request.session['base_url'] + '/stream', 'id' : 'stream'}, context_instance=RequestContext(request))], [])
            
        elif request.method == 'POST':
            # POST request
            form = StrForm(request.POST, error_class=ErrorClear)
            form.fields['isVideo'].initial = False
            form.fields['srcIP'].initial = request.META['REMOTE_ADDR']
            form.fields['srcPort'].initial = 9000
            form.fields['vStream'].choices = self.userVideos(request)

            # Check if the form data is valid and try to start the streaming
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
                        Message.pushMessage(request, Message.ERROR,'Video type not supported')

                    if clvc is not None:
                        vStream = streaming(src=form.cleaned_data['srcIP'], port=form.cleaned_data['srcPort'], mux=form.cleaned_data['srcMux'], vMode=form.cleaned_data['isVideo'], pid=cvlc.pid,video=v, owner=request.session['user'])
                        vStream.save()
                        Message.pushMessage(request, Message.INFO,'Video streaming')
                elif form.cleaned_data['isVideo'] is False:
                    if form.cleaned_data['srcMux'] != "ffmpeg{mux=flv}" and form.cleaned_data['srcMux'] != "webm" and form.cleaned_data['srcMux'] != "ogg":
                        Message.pushMessage(request, Message.ERROR,'Video type not supported')
                    else:
                        cvlc = subprocess.Popen(["/usr/bin/cvlc http://" + str(form.cleaned_data['srcIP']) + ":" + str(form.cleaned_data['srcPort']) + " --sout '#http{mux=" + str(form.cleaned_data['srcMux']) + ",dst=" + request.session['strIP'] + ":" + request.session['strPort'] + "/} -no-sout-rtp-sap -no-sout-standard-sap -sout-keep' --ttl 12"],
                                                shell=True)
                        vStream = streaming(src=form.cleaned_data['srcIP'], port=form.cleaned_data['srcPort'], mux=form.cleaned_data['srcMux'], vMode=form.cleaned_data['isVideo'], pid=cvlc.pid,video=v, owner=request.session['user'])
                        vStream.save()
                        Message.pushMessage(request, Message.ERROR, 'External video streaming.')
                else:
                    Message.pushMessage(request, Message.ERROR, 'If you select the video mode you must select a video.')
                # os.waitpid(p.pid, 0)[1]
                self.render = HttpResponseRedirect('/streaming')
            else:
                for error in form.errors:
                    Message.pushMessage(request, Message.ERROR, 'Error en ' + error + ': ' + str(form._errors[error]))
                if request.META.get('HTTP_REFERER', False) is not False:
                    self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
                else:
                    self.render = HttpResponseRedirect('/index')
        else:
            raise Http404

    def userVideos(self, request):
        '''This method return the videos owned by the actual user.'''
        init = []
        try:
            videos = video.objects.filter(owner=request.session['user'])
            for v in videos:
                init.append((v.idVideo, v.name))
        except video.DoesNotExist:
            pass
        return init

    def getRender(self):
        '''This method return the html rendered'''
        return self.render

class VideoController():
    '''Class to implement the Video controller'''

    # Definition of the video actions
    LIST = 0
    VIEW = 1
    DELETE = 2
    REFERENCE = 3

    def __init__(self, request, action=0, key=None):
        if request.session.get('isConfig', False) is False:
            Config.getSession(request.session)

        # Blocks assigned to the left area
        leftBlocks = []
        if not request.session['user'].is_authenticated():
            leftBlocks = [render_to_string('kirinki/section.html', {'title' : 'login', 'content': render_to_string('kirinki/form.html', {'form' : LoginForm(), 'action' : request.session['base_url'] + '/login'}, context_instance=RequestContext(request))})]
        else:
            try:
                myVideos = video.objects.filter(owner = request.session['user'])
                leftBlocks = [render_to_string('kirinki/section.html', {'title' : 'Mis vídeos', 'content' : render_to_string('kirinki/myVideo.html', {'videos' : myVideos, 'session' : request.session}).encode('utf-8')})]
            except video.DoesNotExist:
                pass

        # Blocks assigned to the center area
        centerBlocks = []
        if action == self.LIST:
            try:
                videoList = video.objects.all()
                centerBlocks = [render_to_string('kirinki/section.html', {'title' : 'Lista de videos', 'content': render_to_string('kirinki/videoList.html', {'videos' : videoList, 'session' : request.session}).encode('utf-8')})]
            except video.DoesNotExist:
                pass
        elif action == self.VIEW:
            if key is not None:
                try:
                    v = video.objects.get(idVideo=key)
                    bfile = '/media/'+v.path[v.path.rfind('/')+1:v.path.rfind('.')]
                    src = {'orig' : request.session['base_url'] + '/media/'+v.path[v.path.rfind('/')+1:]}
                    if os.path.exists(v.path[:v.path.rfind('.')]+'.ogv'):
                        src['ogv'] = request.session['base_url'] +bfile+'.ogv'
                    if os.path.exists(v.path[:v.path.rfind('.')]+'.webm'):
                        src['webm'] = request.session['base_url'] +bfile+'.webm'
                    if os.path.exists(v.path[:v.path.rfind('.')]+'.mp4'):
                        src['mp4'] = request.session['base_url'] +bfile+'.mp4'
                    if os.path.exists(v.path[:v.path.rfind('.')]+'.flv'):
                        src['flv'] = request.session['base_url'] +bfile+'.flv'
                    src['flash'] = request.session['base_url']+'/static/flowplayer/flowplayer-3.2.5.swf'
                    src['flash_str'] = request.session['base_url']+'/static/flowplayer.pseudostreaming/flowplayer.pseudostreaming-3.2.5.swf'
                    centerBlocks = [render_to_string('kirinki/section.html', {'title' : v.name, 'content': render_to_string('kirinki/video.html', {'controls' : True, 'src' : src})})]
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
        elif action == self.REFERENCE:
            pass
        else:
            # Error. Action not defined
            raise Http404

        # Blocks assigned to the right area
        # Ultimos subidos, ultimos usuarios que han subido, usuarios que mas han subido, ...
        rightBlocks = []

        self.render = MainViewer(request).render(leftBlocks, centerBlocks, rightBlocks)

    def getRender(self):
        '''This method returns the html generated'''
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
    convertMP4 = forms.BooleanField(label='Convertir a mp4',
                                    required=False)
    convertOGG = forms.BooleanField(label='Convertir a ogg',
                                    required=False)
    convertWEBM = forms.BooleanField(label='Convertir a webm',
                                     required=False)

class UploadController():
    '''Class to implement the Upload controller. This class will be merged with the VideoController'''
    def __init__(self, request):
        if request.session.get('isConfig', False) is False:
            Config.getSession(request.session)

        if request.method == 'GET':
            # GET request
            leftBlocks = [self.getMyVideos(request.session)]
            centerBlocks = [self.getUploadVideo(request.session['base_url'], request)]
            self.render = MainViewer(request).render(leftBlocks, centerBlocks, [])
            
        elif request.method == 'POST':
            # POST request.
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
                    if form.cleaned_data['convertMP4'] and path[v.path.rfind('.'):].lower() != 'mp4':
                        pass
                    if form.cleaned_data['convertOGG'] and path[v.path.rfind('.'):].lower() != 'ogg':
                        pass
                    if form.cleaned_data['convertWEBM'] and path[v.path.rfind('.'):].lower() != 'web':
                        pass
                    if path[v.path.rfind('.'):].lower() != 'flv':
                        pass
            else:
                for error in form.errors:
                    Message.pushMessage(request, Message.ERROR, 'Error en ' + error + ': ' + str(form._errors[error]))
            if request.META.get('HTTP_REFERER', False) is not False:
                self.render = HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                self.render = HttpResponseRedirect('/index')            
        else:
            raise Http404

    def getMyVideos(self, session):
        '''This method return the videos owned by the actual user.'''
        content = ''
        try:
            myVideos = video.objects.filter(owner = session['user'])
            content = render_to_string('kirinki/myVideo.html', {'videos' : myVideos, 'session' : session}).encode('utf-8')
        except video.DoesNotExist:
            pass
        return render_to_string('kirinki/section.html', {'title' : 'Mis vídeos', 'content' : content})

    def getUploadVideo(self, base_url, request):
        content = render_to_string('kirinki/form.html', {'form' : UploadForm(request.POST, request.FILES, error_class=ErrorClear), 'action' : base_url + '/upload', 'upload' : True}, context_instance=RequestContext(request))
        return render_to_string('kirinki/section.html', {'title' : 'Subir vídeo', 'content' : content})

    def getRender(self):
        '''This method returns the html generated'''
        return self.render
