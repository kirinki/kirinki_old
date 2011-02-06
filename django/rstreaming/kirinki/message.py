# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

# Django Imports
from django.contrib import messages

class Message():
    '''This class manage the stack for the messages shown to the user.'''
    INFO = messages.INFO
    ERROR = messages.ERROR
    
    @staticmethod
    def pushMessage(request, msgType, msg):
        messages.set_level(request, msgType)
        messages.add_message(request, msgType, msg)
