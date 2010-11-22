#!/usr/bin/env python

import web
from rstr_database import *

urls = (
  '/', 'index',
  '/about', 'about'
)

app = web.application(urls, globals())
web.config.debug = True
session = {}

conf = {'dbtype' : 'postgres', 'dbname' : 'rstreaming', 'dbuser' : 'i02sopop', 'dbpasswd' : ''}

class config:
    """ Configuration class. We have access to all the configs throw this class. """    
    def __init__(self):
        global conf
        self.cfg = conf
        self.db = web.database(dbn=conf['dbtype'], db=conf['dbname'], user=conf['dbuser'], pw=conf['dbpasswd'])
    
    def getConfig(self, cfgName):
        return self.cfg[cfgName]
    
    def setConfig(self, cfgName, cfgValue):
        self.cfg[cfgName] = cfgValue

    def __getitem__(self, key):
        return self.cfg[key]

    def __setitem__(self, key, value):
        self.cfg[key] = value

# Load the session
if web.config.debug:
    if web.config.get('_session') is None:
        conf = config()
        db = web.database(dbn=conf.getConfig('dbtype'), db=conf.getConfig('dbname'), user=conf.getConfig('dbuser'), pw=conf.getConfig('dbpasswd'))
        store = web.session.DBStore(db, 'sessions')
        session = web.session.Session(app, store, {'cfg' : conf})
        web.config._session = session
    else:
        session = web.config._session
else:
    conf = config()
    db = web.database(dbn=conf.getConfig('dbtype'), db=conf.getConfig('dbname'), user=conf.getConfig('dbuser'), pw=conf.getConfig('dbpasswd'))
    store = web.session.DBStore(db, 'sessions')
    session = web.session.Session(app, store, initializer={'cfg' : conf})

if not 'cfg' in session:
    session['cfg'] = config()
