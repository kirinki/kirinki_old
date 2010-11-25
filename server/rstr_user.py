#!/usr/bin/env python
# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

import logging
import web
from web import form

from rstr_config import conf

class user:
    """User class"""
    def __init__(self):
        self.data = {'id' : -1, 'username' : '', 'password' : '', 'name' : '', 'surname' : '', 'email' : '', 'videos' : [], 'userType' : 1, 'logged' : False }

    def checkUsername(self,user):
        return True

    def login(self, user, passwd):
        logging.debug('data: 0')
        db = web.database(host=conf['dbhost'],dbn=conf['dbtype'], db=conf['dbname'], user=conf['dbuser'], pw=conf['dbpasswd'])
        logging.debug('data: 1')
        myvar = dict(username=user)
        ident = db.select('usr', myvar, where="username = $username")
        results = ident[0]
        logging.debug(results)
        if passwd == results['password']:
            self.id = results['idusr']
            self.username = results['username']
            self.password = results['password']
            self.name = results['name']
            self.surname = results['surname']
            self.email = results['email']
            self.userType = results['usrtype']
            self.logged = True
            usrVideos = db.query("select id from video where id_owner = '%d'" % (self.id)).getresult()
            #for idVideo in usrVideos:
                #self.videos.append(video(idVideo[0]))
            return True
        return False

    def loginForm(self):
        login = form.Form(form.Textbox('username'),
                          form.Password('password'),
                          validators = [form.Validator("Debe de ingresar el usuario.", lambda i: i.username is not None and i.username != ''),
                                        form.Validator("Debe de ingresar la contrasena.", lambda i: i.password is not None and i.password != '')])
        self.lForm = login()
        return self.lForm
        
    def regForm(self):
        register = form.Form(form.Textbox('username'),
                             form.Password('password'),
                             form.Password('password_again'),
                             validators = [form.Validator("Las contrasenas no coinciden.", lambda i: i.password == i.password_again),
                                           form.Validator("El nombre de usuario seleccionado ya existe", lambda i: not session['usr'].checkUsername(i.username))])
        self.rForm = register()
        return self.rForm

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
