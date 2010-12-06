# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

import logging
from django.contrib import messages
from django.template import RequestContext
from django.template.loader import render_to_string

from rstr.config import Config
from rstr.mainviewer import MainViewer
from rstr.user import LoginForm

class IndexView():
    def __init__(self, request):
        logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)
        messages.set_level(request, messages.INFO)
        #request.session.clear()
        if request.session.get('isConfig', False) is False:
            request.session.set_expiry(600)
            data = Config(request.session).getSessionData()
            request.session.update(data)
            request.session['isConfig'] = True
        leftBlocks = []
        if not request.session['user'].is_authenticated():
            leftBlocks = [render_to_string('rstr/section.html', {'title' : 'login', 'content': render_to_string('rstr/form.html', {'form' : LoginForm(), 'session' : request.session}, context_instance=RequestContext(request))})]
        centerBlocks = [render_to_string('rstr/section.html', {'title' : 'Bienvenido', 'content' : 'Bienvenido a Ritho\'s Streaming, el sitio desde el cual podras hacer Streaming tanto en directo como en diferido de manera sencilla..'})]
        rightBlocks = [self.generateArticles(), self.generateVideos()]
        self.render = MainViewer(request).render(leftBlocks, centerBlocks, rightBlocks)

    def generateArticles(self):
        # article = render_to_string('rstr/article.html', {'title' : 'Inicio del proyecto', 'date' : '2010-12-01','abstract' : 'Con la inauguracion de esta oficial comienza su andadura el proyecto.', 'content' : 'Explicacion del proyecto RStreaming'})
        # return render_to_string('rstr/section.html', {'title' : 'Ultimas noticias', 'content' : article})
        return ''

    def generateVideos(self):
        # videos = render_to_string('rstr/video.html', {'width' : '320', 'height' : '240', 'controls' : True, 'src': 'file:///home/i02sopop/Downloads/PiTP - 2009 - Monday, July 13, 2009 - Kernighan.hi.mp4'})
        # return render_to_string('rstr/section.html', {'title' : 'Videos', 'content' : videos})
        return ''


    def getRender(self):
        return self.render
