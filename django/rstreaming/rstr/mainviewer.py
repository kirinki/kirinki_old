# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

from django.core.cache import cache
from django.contrib.sessions.models import Session
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from recaptcha.client import captcha
from datetime import datetime, timedelta
from rstr.models import video
import logging

class MainViewer:
    def __init__(self, req):
        logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
        self.request = req
        self.session_data = req.session
        
    def getViewer(self, out):
        leftBlocks = []
        centerBlocks = []
        rightBlocks = []

        if out == 'register':
            if not self.session_data['user'].is_authenticated():
                centerBlocks = [render_to_string('rstr/section.html', {'title' : 'Register', 'content': render_to_string('rstr/register.html', {'session' : self.session_data, 'captcha' : captcha.displayhtml('6LefRr8SAAAAAMncFelaGsop60Uuon0MCL6H-aP3')}, context_instance=RequestContext(self.request))})]

        elif out == 'videos':
            if not self.session_data['user'].is_authenticated():
                leftBlocks = [render_to_string('rstr/section.html', {'title' : 'login', 'content': render_to_string('rstr/login.html', {'session' : self.session_data}, context_instance=RequestContext(self.request))})]

        elif out == 'logout':
            pass

        elif out == 'streaming':
            if not self.session_data['user'].is_authenticated():
                leftBlocks = [render_to_string('rstr/section.html', {'title' : 'login', 'content': render_to_string('rstr/login.html', {'session' : self.session_data}, context_instance=RequestContext(self.request))})]

        elif out == 'stream':
            pass

        elif out == 'upload':
            leftBlocks = [self.getMyVideos()]
            centerBlocks = [self.getUploadVideo()]

        elif out == 'admin':
            pass

        elif out == 'account':
            pass

        else:
            raise Http404

        return self.render(leftBlocks, centerBlocks, rightBlocks)

    def getLeftCol(self, blocks = []):
        return render_to_string('rstr/left.html', {'blocks' : blocks})

    def getCenterCol(self, blocks = []):
        return render_to_string('rstr/center.html', {'blocks' : blocks})

    def getRightCol(self, blocks = []):
        return render_to_string('rstr/right.html', {'blocks' : blocks})

    def getMyVideos(self):
        content = ''
        try:
            myVideos = video.objects.filter(id_owner = self.session_data['user'])
            content = render_to_string('rstr/myVideo.html', {'videos' : myVideos, 'session' : self.session_data}).encode('utf-8')
        except video.DoesNotExist:
            pass
        return render_to_string('rstr/section.html', {'title' : 'Mis vídeos', 'content' : content})

    def getUploadVideo(self):
        content = render_to_string('rstr/uploadVideo.html', {'session' : self.session_data})
        return render_to_string('rstr/section.html', {'title' : 'Subir vídeo', 'content' : content})

    def render(self, leftBlocks, centerBlocks, rightBlocks):
        self.page = render_to_response('rstr/index.html', {'copy' : '&copy; Pablo Alvarez de Sotomayor Posadillo',
                                                           'session' : self.session_data,
                                                           'leftCol' : self.getLeftCol(leftBlocks),
                                                           'centerCol' : self.getCenterCol(centerBlocks),
                                                           'rightCol' : self.getRightCol(rightBlocks)}, context_instance=RequestContext(self.request))
        return self.page
