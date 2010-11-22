#!/usr/bin/env python

from rstr_config import *
from rstr_user import *

cfg = session['cfg']

if not 'usr' in session:
    session['usr'] = user()
usr = session['usr']

if not 'db' in session:
    session['db'] = database(cfg['dbtype'],
                             cfg['dbname'],
                             cfg['dbuser'],
                             cfg['dbpasswd'])
db = session['db']

render = web.template.render('/home/i02sopop/desarrollo/rstreaming/server/templates/', globals={'context': session})
