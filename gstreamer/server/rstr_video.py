#!/usr/bin/env python
# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

class video:
    def __init__(self):
        self.data = {'id' : -1}

    def __init__(self, idVideo):
        self.data = {'id' : idVideo}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
