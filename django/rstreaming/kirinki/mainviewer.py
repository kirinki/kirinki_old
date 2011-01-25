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
import logging

class MainViewer:
    def __init__(self, req):
        logging.basicConfig(filename='/var/log/kirinki.log',level=logging.DEBUG)
        self.request = req
        self.session_data = req.session
        
    def getLeftCol(self, blocks = []):
        return render_to_string('kirinki/left.html', {'blocks' : blocks})

    def getCenterCol(self, blocks = []):
        return render_to_string('kirinki/center.html', {'blocks' : blocks})

    def getRightCol(self, blocks = []):
        return render_to_string('kirinki/right.html', {'blocks' : blocks})

    def render(self, leftBlocks, centerBlocks, rightBlocks):
        self.page = render_to_response('kirinki/index.html', {'copy' : '&copy; Pablo Alvarez de Sotomayor Posadillo',
                                                           'session' : self.session_data,
                                                           'leftCol' : self.getLeftCol(leftBlocks),
                                                           'centerCol' : self.getCenterCol(centerBlocks),
                                                           'rightCol' : self.getRightCol(rightBlocks)}, context_instance=RequestContext(self.request))
        return self.page
