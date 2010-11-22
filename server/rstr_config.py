#!/usr/bin/env python

import web
from rstr_database import *

conf = {'dbtype' : 'postgres',
        'dbname' : 'rstreaming',
        'dbuser' : 'i02sopop',
        'dbpasswd' : ''}

urls = (
  '/', 'index',
  '/about', 'about'
)

app = web.application(urls, globals())
web.config.debug = True
session = {}

class config:
    """ Configuration class. We have access to all the configs throw this class. """    
    def __init__(self):
        global conf
        self.data = conf
        db = web.database(dbn=conf['dbtype'], db=conf['dbname'], user=conf['dbuser'], pw=conf['dbpasswd'])
        cfgs = db.select('configs')
        for cfg in cfgs:
            self[cfg['cfghey']] = cfg['cfgvalue']

    def save(self):
        db = web.database(dbn=conf['dbtype'], db=conf['dbname'], user=conf['dbuser'], pw=conf['dbpasswd'])
        for key:value in data:
            res = db.query("SELECT key FROM configs WHERE key = '"+value+"'")
            if res.count() > 0:
                self.db.update('configs', where='cfgkey = '+key, cfgvalue=value)
            else:
                self.db.insert('configs', cfgkey=key, cfgvalue=value)
        
    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

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

if not 'cfg' in session:
    session['cfg'] = config()
