from django.db import models

# Create your models here.
class usrType(models.Model):
    idType = models.AutoField(primary_key=True)
    tName = models.CharField(max_length=50, unique=True)
    tDescription = models.CharField(max_length=200)

    def __unicode__(self):
        return self.tName

class usr(models.Model):
    idUsr = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    signup_date = models.DateTimeField('signup date')
    last_sign_date = models.DateTimeField('lastsign date')
    usrType = models.ForeignKey(usrType)

    def __unicode__(self):
        return self.username

class video(models.Model):
    idVideo = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=250)
    format = models.CharField(max_length=20)
    pub_date = models.DateTimeField('date published')
    id_owner = models.ForeignKey(usr)

    def __unicode__(self):
        return self.name

class configs(models.Model):
    cfgkey = models.CharField(max_length=50)
    cfgvalue = models.CharField(max_length=200)

    def __unicode__(self):
        return self.cfgkey
