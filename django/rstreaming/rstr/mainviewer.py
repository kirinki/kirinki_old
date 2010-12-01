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
                leftBlocks = [render_to_string('rstr/login.html', {'session' : self.session_data}, context_instance=RequestContext(self.request))]
            self.page = render_to_response('rstr/index.html', {'copy' : '&copy; Pablo Alvarez de Sotomayor Posadillo',
                                                               'session' : self.session_data,
                                                               'leftCol' : self.getLeftCol(leftBlocks),
                                                               'centerCol' : self.getCenterCol(),
                                                               'rightCol' : self.getRightCol()}, context_instance=RequestContext(self.request))
        elif out == 'login':
            self.page = render_to_response('rstr/index.html', {'copy' : '&copy; Pablo Alvarez de Sotomayor Posadillo',
                                                               'session' : self.session_data,
                                                               'leftCol' : self.getLeftCol(),
                                                               'centerCol' : self.getCenterCol(),
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
        return render_to_string('rstr/center.html', {})

    def getRightCol(self, blocks = []):
        return render_to_string('rstr/right.html', {})
