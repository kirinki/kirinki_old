# -*- coding: utf-8 -*-
__license__ = "GNU Affero General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

# This file is part of Kirinki.
# 
# Kirinki is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as 
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# Kirinki is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public
# License along with kirinki. If not, see <http://www.gnu.org/licenses/>.

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
