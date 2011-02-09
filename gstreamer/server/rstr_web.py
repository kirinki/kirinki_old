#!/usr/bin/env python
# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

import sys, os
abspath = '/home/i02sopop/desarrollo/rstreaming/server/'
sys.path.append(abspath)
os.chdir(abspath)

import logging
import web
from web import form

from rstr_database import *
from rstr_config import *
from rstr_user import *

web.config.debug = True

urls = (
  '/', 'Index',
  '/about', 'About',
  '/user', 'User',
  '/login', 'Login',
  '/logout', 'Logout',
  '/register','Register'
)

app = web.application(urls, globals())

# Load the session
if web.config.debug:
    if web.config.get('_session') is None:
        conf = config()
        db = web.database(dbn=conf['dbtype'], db=conf['dbname'], user=conf['dbuser'], pw=conf['dbpasswd'])
        store = web.session.DBStore(db, 'sessions')
        session = web.session.Session(app, store, {'cfg' : conf})
        web.config._session = session
    else:
        session = web.config._session
else:
    conf = config()
    db = web.database(dbn=conf['dbtype'], db=conf['dbname'], user=conf['dbuser'], pw=conf['dbpasswd'])
    store = web.session.DBStore(db, 'sessions')
    session = web.session.Session(app, store, initializer={'cfg' : conf})

logging.basicConfig(filename=conf['logfile'],level=logging.DEBUG)

if not 'cfg' in session:
    session['cfg'] = config()
if not 'usr' in session:
    session['usr'] = user()
if not 'db' in session:
    cfg = session['cfg']
    session['db'] = database(cfg['dbtype'],
                             cfg['dbname'],
                             cfg['dbuser'],
                             cfg['dbpasswd'])

render = web.template.render('templates/', globals={'user': session['usr']})
session['render'] = render

def session_hook():
    web.ctx.session = session
web.ctx.session = session

app.add_processor(web.loadhook(session_hook))

from rstr_action_about import *
from rstr_action_index import *
from rstr_action_login import *
from rstr_action_logout import *
from rstr_action_register import *
from rstr_action_user import *

application = web.application(urls, globals()).wsgifunc()
#if __name__ == "__main__": app.run()
