# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

from django.core.cache import cache
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from rstr.models import configs
import logging

class Config:
    def __init__(self, key):
        logging.basicConfig(filename='/var/log/rstreaming.log',level=logging.DEBUG)

        if not cache.get('numUsers', False):
            cache.set('numUsers', 1)
        else:
            cache.incr('numUsers')
            # cache.decr('numUsers')

        try:
            s = Session.objects.get(pk=key)
        except ObjectDoesNotExist:
            s = Session()

        session_data = s.get_decoded()
        if not session_data.get('user', False):
            session_data['user'] = AnonymousUser()

        cfgs = configs.objects.all()
        for cfg in cfgs:
            logging.debug(cfg.cfgkey)
            logging.debug(cfg.cfgvalue)
            session_data[cfg.cfgkey.encode('utf-8')] = cfg.cfgvalue.encode('utf-8')

        self.data = session_data
        s.session_data=Session.objects.encode(session_data)
        s.save()

    def getSessionData(self):
        return self.data
