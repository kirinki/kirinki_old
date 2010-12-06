# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

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

class streaming(models.Model):
    idVideo = models.AutoField(primary_key=True)
    src = models.CharField(max_length=100)
    dest = models.CharField(max_length=100)
    id_owner = models.ForeignKey(User)

    def __unicode__(self):
        return self.cfgkey

class video(models.Model):
    idVideo = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=250)
    path = models.CharField(max_length=250)
    format = models.CharField(max_length=20)
    pub_date = models.DateTimeField('date published')
    id_owner = models.ForeignKey(User)

    def __unicode__(self):
        return self.name
