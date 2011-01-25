# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

from django.forms.util import ErrorList

class ErrorClear(ErrorList):
    def __str__(self):
        return self.as_clear().encode('utf-8')
    def as_clear(self):
        if not self:
            return ''
        return ''.join(['%s' % e for e in self])

