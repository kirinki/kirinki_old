#!/usr/bin/env python
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

import sys, os
abspath = '/home/i02sopop/desarrollo/rstreaming/server/'
sys.path.append(abspath)
os.chdir(abspath)

import web
from web import form

from rstr_database import *
from rstr_config import *
from rstr_user import *

urls = (
  '/', 'index',
  '/about', 'about',
  '/login', 'login',
  '/logout', 'logout',
  '/register','register'
)

app = web.application(urls, globals())

# Load the session
if web.config.debug:
    if web.config.get('_session') is None:
        conf = config()
        db = web.database(dbn=conf['dbtype'], db=conf['dbname'], user=conf['dbuser'], pw=conf['dbpasswd'])
        store = web.session.DBStore(db, 'sessions')
        web.ctx.session = web.session.Session(app, store, {'cfg' : conf})
        web.config._session = web.ctx.session
    else:
        web.ctx.session = web.config._session
else:
    conf = config()
    db = web.database(dbn=conf['dbtype'], db=conf['dbname'], user=conf['dbuser'], pw=conf['dbpasswd'])
    store = web.session.DBStore(db, 'sessions')
    web.ctx.session = web.session.Session(app, store, initializer={'cfg' : conf})

if not 'cfg' in web.ctx.session:
    web.ctx.session['cfg'] = config()
if not 'usr' in web.ctx.session:
    web.ctx.session['usr'] = user()
if not 'db' in web.ctx.session:
    cfg = web.ctx.session['cfg']
    web.ctx.session['db'] = database(cfg['dbtype'],
                                     cfg['dbname'],
                                     cfg['dbuser'],
                                     cfg['dbpasswd'])

render = web.template.render('templates/', globals={'user': web.ctx.session['usr']})
web.ctx.session['render'] = render

from rstr_action_index import *
from rstr_action_about import *
from rstr_action_login import *
from rstr_action_logout import *
from rstr_action_register import *

application = web.application(urls, globals()).wsgifunc()
#if __name__ == "__main__": app.run()

# db = web.database(dbn='postgres', user='username', pw='password', db='dbname')
# todos = db.select('todo')
# return render.index(todos)
# post_data=web.input(name=[])
# n = db.insert('todo', title=data.title)
# raise web.seeother('/'+data.name)
