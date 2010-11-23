#!/usr/bin/env python

class video:
    def __init__(self):
        self.data = {'id' : -1}

    def __init__(self, idVideo):
        self.data = {'id' : idVideo}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
