#!/usr/bin/env python
# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

import web

class database:
    """ Database class """
    def __init__(self, dbtype, dbname, dbusr, dbpasswd):
        self.dbtype = dbtype
        self.dbname = dbname
        self.dbusr = dbusr
        self.dbpasswd = dbpasswd
        self.connect()

    def connect(self):
        self.db = web.database(dbn=self.dbtype, db=self.dbname, user=self.dbusr, pw=self.dbpasswd)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
