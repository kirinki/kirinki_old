#!/usr/bin/env python

import web
from rstr_config import *

class database:
    """ Database class """
    def __init__(self, dbtype, dbname, dbusr, dbpasswd):
        self.dbtype = dbtype
        self.dbname = dbname
        self.dbusr = dbusr
        self.dbpasswd = dbpasswd

    def connect():
        self.db = web.database(dbn=self.dbtype, db=self.dbname, user=self.dbuser, pw=self.dbpasswd)
