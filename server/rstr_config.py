#!/usr/bin/env python

import web

web.config.debug = True
conf = {'dbtype' : 'postgres',
        'dbhost' : 'localhost',
        'dbname' : 'rstreaming',
        'dbuser' : 'i02sopop',
        'dbpasswd' : 'passwd'}

class config:
    """ Configuration class. We have access to all the configs throw this class. """    
    def __init__(self):
        global conf
        self.data = conf
        db = web.database(host=conf['dbhost'],dbn=conf['dbtype'], db=conf['dbname'], user=conf['dbuser'], pw=conf['dbpasswd'])
        cfgs = db.select('configs')
        for cfg in cfgs:
            self[cfg['cfgkey']] = cfg['cfgvalue']

    def save(self):
        db = web.database(dbn=conf['dbtype'], db=conf['dbname'], user=conf['dbuser'], pw=conf['dbpasswd'])
        for key,value in data:
            res = db.query("SELECT key FROM configs WHERE key = '"+value+"'")
            if res.count() > 0:
                self.db.update('configs', where='cfgkey = '+key, cfgvalue=value)
            else:
                self.db.insert('configs', cfgkey=key, cfgvalue=value)
        
    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

