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
