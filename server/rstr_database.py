#!/usr/bin/env python

import web

class database:
    """ Database class """
    def __init__(self, dbtype, dbname, dbusr, dbpasswd):
        self.dbtype = dbtype
        self.dbname = dbname
        self.dbusr = dbusr
        self.dbpasswd = dbpasswd

    def connect():
        self.db = web.database(dbn=self.dbtype, db=self.dbname, user=self.dbuser, pw=self.dbpasswd)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
