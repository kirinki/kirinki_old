# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

from django.core.cache import cache
from django.contrib.sessions.models import Session
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from recaptcha.client import captcha
import logging

class MainViewer:
    def __init__(self, req, key):
        logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)

        s = Session.objects.get(pk=key)
        self.session_data = s.get_decoded()
        self.request = req
        
    def getViewer(self, out):
        leftBlocks = []
        centerBlocks = []
        rightBlocks = []

        if out == 'index':
            if not self.session_data['user'].is_authenticated():
                leftBlocks = [render_to_string('rstr/section.html', {'title' : 'login', 'content': render_to_string('rstr/login.html', {'session' : self.session_data}, context_instance=RequestContext(self.request))})]
            centerBlocks = [render_to_string('rstr/section.html', {'title' : 'Bienvenido', 'content' : 'Bienvenido al sitio web de Ritho.'})]
            rightBlocks = [self.generateArticles(), self.generateVideos()]

        elif out == 'login':
            if not self.session_data['user'].is_authenticated():
                centerBlocks = [render_to_string('rstr/section.html', {'title' : 'Login', 'content': render_to_string('rstr/login.html', {'session' : self.session_data}, context_instance=RequestContext(self.request))})]

        elif out == 'register':
            if not self.session_data['user'].is_authenticated():
                centerBlocks = [render_to_string('rstr/section.html', {'title' : 'Register', 'content': render_to_string('rstr/register.html', {'session' : self.session_data, 'captcha' : captcha.displayhtml('6LefRr8SAAAAAMncFelaGsop60Uuon0MCL6H-aP3')}, context_instance=RequestContext(self.request))})]

        elif out == 'videos':
            if not self.session_data['user'].is_authenticated():
                leftBlocks = [render_to_string('rstr/section.html', {'title' : 'login', 'content': render_to_string('rstr/login.html', {'session' : self.session_data}, context_instance=RequestContext(self.request))})]
            centerBlocks = [render_to_string('rstr/section.html', {'title' : 'Bienvenido', 'content' : 'Bienvenido al sitio web de Ritho.'})]
            rightBlocks = [self.generateArticles(), self.generateVideos()]

        elif out == 'logout':
            if not self.session_data['user'].is_authenticated():
                leftBlocks = [render_to_string('rstr/section.html', {'title' : 'login', 'content': render_to_string('rstr/login.html', {'session' : self.session_data}, context_instance=RequestContext(self.request))})]
            centerBlocks = [render_to_string('rstr/section.html', {'title' : 'Bienvenido', 'content' : 'Bienvenido al sitio web de Ritho.'})]
            rightBlocks = [self.generateArticles(), self.generateVideos()]

        elif out == 'streaming':
            if not self.session_data['user'].is_authenticated():
                leftBlocks = [render_to_string('rstr/section.html', {'title' : 'login', 'content': render_to_string('rstr/login.html', {'session' : self.session_data}, context_instance=RequestContext(self.request))})]
            centerBlocks = [render_to_string('rstr/section.html', {'title' : 'Bienvenido', 'content' : 'Bienvenido al sitio web de Ritho.'})]
            rightBlocks = [self.generateArticles(), self.generateVideos()]

        elif out == 'stream':
            if not self.session_data['user'].is_authenticated():
                leftBlocks = [render_to_string('rstr/section.html', {'title' : 'login', 'content': render_to_string('rstr/login.html', {'session' : self.session_data}, context_instance=RequestContext(self.request))})]
            centerBlocks = [render_to_string('rstr/section.html', {'title' : 'Bienvenido', 'content' : 'Bienvenido al sitio web de Ritho.'})]
            rightBlocks = [self.generateArticles(), self.generateVideos()]

        elif out == 'upload':
            # Mis videos
            leftBlocks = []
            # Subir videos
            centerBlocks = []

        elif out == 'admin':
            if not self.session_data['user'].is_authenticated():
                leftBlocks = [render_to_string('rstr/section.html', {'title' : 'login', 'content': render_to_string('rstr/login.html', {'session' : self.session_data}, context_instance=RequestContext(self.request))})]
            centerBlocks = [render_to_string('rstr/section.html', {'title' : 'Bienvenido', 'content' : 'Bienvenido al sitio web de Ritho.'})]
            rightBlocks = [self.generateArticles(), self.generateVideos()]

        elif out == 'account':
            if not self.session_data['user'].is_authenticated():
                leftBlocks = [render_to_string('rstr/section.html', {'title' : 'login', 'content': render_to_string('rstr/login.html', {'session' : self.session_data}, context_instance=RequestContext(self.request))})]
            centerBlocks = [render_to_string('rstr/section.html', {'title' : 'Bienvenido', 'content' : 'Bienvenido al sitio web de Ritho.'})]
            rightBlocks = [self.generateArticles(), self.generateVideos()]

        else:
            raise Http404

        self.page = render_to_response('rstr/index.html', {'copy' : '&copy; Pablo Alvarez de Sotomayor Posadillo',
                                                           'session' : self.session_data,
                                                           'leftCol' : self.getLeftCol(leftBlocks),
                                                           'centerCol' : self.getCenterCol(centerBlocks),
                                                           'rightCol' : self.getRightCol(rightBlocks)}, context_instance=RequestContext(self.request))
        return self.page

    def getLeftCol(self, blocks = []):
        return render_to_string('rstr/left.html', {'blocks' : blocks})

    def getCenterCol(self, blocks = []):
        return render_to_string('rstr/center.html', {'blocks' : blocks})

    def getRightCol(self, blocks = []):
        return render_to_string('rstr/right.html', {'blocks' : blocks})

    def generateArticles(self):
        article = render_to_string('rstr/article.html', {'title' : 'Inicio del proyecto', 'date' : '2010-12-01','abstract' : 'Con la inauguracion de esta oficial comienza su andadura el proyecto.', 'content' : 'Explicacion del proyecto RStreaming'})
        return render_to_string('rstr/section.html', {'title' : 'Ultimas noticias', 'content' : article})

    def generateVideos(self):
        videos = render_to_string('rstr/video.html', {'width' : '320', 'height' : '240', 'controls' : True, 'src': 'file:///home/i02sopop/Downloads/PiTP - 2009 - Monday, July 13, 2009 - Kernighan.hi.mp4'})
        return render_to_string('rstr/section.html', {'title' : 'Videos', 'content' : videos})
