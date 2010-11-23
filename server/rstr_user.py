#!/usr/bin/env python

import web
from web import form

class user:
    """User class"""
    def __init__(self):
        self.data = {'id' : -1, 'username' : '', 'password' : '', 'name' : '', 'surname' : '', 'email' : '', 'videos' : [], 'userType' : 1, 'logged' : False }

    def checkUsername(self,user):
        return True

    def login(self,data):
        db = web.ctx.session['db']
        ident = db.query("select * from usr where username = '%s'" % (data.username)).getresult()
        if data.password == ident[0][2]:
            self.id = ident[0][0]
            self.username = ident[0][1]
            self.password = ident[0][2]
            self.name = ident[0][3]
            self.surname = ident[0][4]
            self.email = ident[0][5]
            self.userType = ident[0][6]
            self.logged = True
            usrVideos = db.query("select id from video where id_owner = '%d'" % (self.id)).getresult()
            for idVideo in usrVideos:
                self.videos.append(video(idVideo[0]))
            return True
        return False

    def loginForm(self):
        login = form.Form(form.Textbox('username'),
                          form.Password('password'),
                          validators = [form.Validator("Debe de ingresar el usuario.", lambda i: i.username is not None and i.username != ''),
                                        form.Validator("Debe de ingresar la contrasena.", lambda i: i.password is not None and i.password != ''),
                                        form.Validator("Usuario o contrasena incorrectos.", lambda i: session['usr'].login(i))])
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
