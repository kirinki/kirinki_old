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

from django.db import models
from django.contrib.auth.models import User
 
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()

class configs(models.Model):
    cfgkey = models.CharField(max_length=50)
    cfgvalue = models.CharField(max_length=200)

    def __unicode__(self):
        return self.cfgkey

class video(models.Model):
    idVideo = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=250)
    path = models.CharField(max_length=250)
    format = models.CharField(max_length=20)
    pub_date = models.DateTimeField('date published')
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

class streaming(models.Model):
    idStreaming = models.AutoField(primary_key=True)
    src = models.IPAddressField(null=True)
    port = models.PositiveIntegerField(null=True)
    mux = models.CharField(max_length=20)
    vMode = models.BooleanField()
    video = models.ForeignKey(video, null=True)
    pid =  models.IntegerField()
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return self.cfgkey

