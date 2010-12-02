from django.core.cache import cache
from django.contrib.sessions.models import Session
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
import logging

class MainViewer:
    def __init__(self, req, key):
        logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)

        s = Session.objects.get(pk=key)
        self.session_data = s.get_decoded()
        self.request = req
        
    def getViewer(self, out):
        if out == 'index' or out == 'logout' or out == 'about' or out == 'streaming' or out == 'videos' or out == 'stream' or out == 'upload' or out == 'admin':
            leftBlocks = []
            if not self.session_data['user'].is_authenticated():
                leftBlocks = [render_to_string('rstr/section.html', {'title' : 'login', 'content': render_to_string('rstr/login.html', {'session' : self.session_data}, context_instance=RequestContext(self.request))})]
            centerBlocks = [render_to_string('rstr/section.html', {'title' : 'Bienvenido', 'content' : 'Bienvenido al sitio web de Ritho.'})]
            rightBlocks = [self.generateArticles(), self.generateVideos()]
            self.page = render_to_response('rstr/index.html', {'copy' : '&copy; Pablo Alvarez de Sotomayor Posadillo',
                                                               'session' : self.session_data,
                                                               'leftCol' : self.getLeftCol(leftBlocks),
                                                               'centerCol' : self.getCenterCol(centerBlocks),
                                                               'rightCol' : self.getRightCol(rightBlocks)}, context_instance=RequestContext(self.request))
        elif out == 'login':
            centerBlocks = []
            if not self.session_data['user'].is_authenticated():
                centerBlocks = [render_to_string('rstr/section.html', {'title' : 'login', 'content': render_to_string('rstr/login.html', {'session' : self.session_data}, context_instance=RequestContext(self.request))})]
            self.page = render_to_response('rstr/index.html', {'copy' : '&copy; Pablo Alvarez de Sotomayor Posadillo',
                                                               'session' : self.session_data,
                                                               'leftCol' : self.getLeftCol(),
                                                               'centerCol' : self.getCenterCol(centerBlocks),
                                                               'rightCol' : self.getRightCol()}, context_instance=RequestContext(self.request))
        elif out == 'register':
            self.page = render_to_response('rstr/index.html', {'copy' : '&copy; Pablo Alvarez de Sotomayor Posadillo',
                                                               'session' : self.session_data,
                                                               'leftCol' : self.getLeftCol(),
                                                               'centerCol' : self.getCenterCol(),
                                                               'rightCol' : self.getRightCol()}, context_instance=RequestContext(self.request))
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
