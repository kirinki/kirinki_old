#!/usr/bin/env python

from rstr_config import *
from rstr_user import *

if not 'usr' in session:
    session['usr'] = user()

if not 'db' in session:
    session['db'] = database(session['cfg'].getConfig('dbtype'),
                             session['cfg'].getConfig('dbname'),
                             session['cfg'].getConfig('dbuser'),
                             session['cfg'].getConfig('dbpasswd'))

cfg = session['cfg']
usr = session['usr']
db = session['db']
render = web.template.render('/home/i02sopop/desarrollo/rstreaming/server/templates/', globals={'context': session})

#def session_hook():
#    web.ctx.session = session
#    web.template.Template.globals['session'] = session

#app.add_processor(web.loadhook(session_hook))
