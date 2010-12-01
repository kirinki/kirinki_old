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
        session_data = s.get_decoded()

        blocks = []
        if not session_data['user'].is_authenticated():
            blocks = [render_to_string('rstr/login.html', {'session' : session_data}, context_instance=RequestContext(req))]
        leftCol = render_to_string('rstr/left.html', {'blocks' : blocks})
        centerCol = render_to_string('rstr/center.html', {})
        rightCol = render_to_string('rstr/right.html', {})
        self.page = render_to_response('rstr/index.html', {'copy' : '&copy; Pablo Alvarez de Sotomayor Posadillo',
                                                           'session' : session_data,
                                                           'leftCol' : leftCol,
                                                           'centerCol' : centerCol,
                                                           'rightCol' : rightCol}, context_instance=RequestContext(req))

        s.session_data=Session.objects.encode(session_data)
        s.save()
        
    def getViewer(self):
        return self.page
