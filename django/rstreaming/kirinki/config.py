# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

# Python general imports
from datetime import datetime, timedelta

# Django imports
from django.core.cache import cache
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.models import Session

# Application imports
from kirinki.models import configs
from kirinki.log import Log

class Config:
    '''Class to load and store the site config from/to the database to/from the session'''

    @staticmethod
    def getSession(session):
        if not cache.get('numUsers', False):
            cache.set('numUsers', 1)
        else:
            cache.incr('numUsers')
            # cache.decr('numUsers')

        if not session.get('user', False):
            session['user'] = AnonymousUser()

        cfgs = configs.objects.all()
        data = {}
        for cfg in cfgs:
            Log().debug(cfg.cfgkey)
            Log().debug(cfg.cfgvalue)
            data[cfg.cfgkey.encode('utf-8')] = cfg.cfgvalue.encode('utf-8')

        session.set_expiry(int(data.get('session_expiry',1200)))
        session.update(data)
        session['isConfig'] = True
