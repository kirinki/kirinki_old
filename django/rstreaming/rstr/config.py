# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

from django.core.cache import cache
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.models import Session
from rstr.models import configs
import logging
from datetime import datetime, timedelta

class Config:
    def __init__(self, session):
        logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)

        if not cache.get('numUsers', False):
            cache.set('numUsers', 1)
        else:
            cache.incr('numUsers')
            # cache.decr('numUsers')

        if not session.get('user', False):
            session['user'] = AnonymousUser()

        cfgs = configs.objects.all()
        for cfg in cfgs:
            logging.debug(cfg.cfgkey)
            logging.debug(cfg.cfgvalue)
            session[cfg.cfgkey.encode('utf-8')] = cfg.cfgvalue.encode('utf-8')

        self.data = session

    def getSessionData(self):
        return self.data
