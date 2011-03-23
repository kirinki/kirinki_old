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
