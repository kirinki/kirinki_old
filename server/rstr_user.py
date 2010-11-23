#!/usr/bin/env python

import web
from web import form

class user:
    """User class"""
    def __init__(self):
        self.data = {'username' : '', 'password' : '', 'name' : '', 'surname' : '', 'email' : '', 'videos' : [], 'userType' : 1, 'logged' : False }

    def checkUsername(user):
        return True

    def login(data):
        return True

    def loginForm(self):
        login = form.Form(form.Textbox('username'),
                          form.Password('password'),
                          validators = [form.Validator("Usuario o contrasena incorrectos.", lambda i: session['usr'].login(i))])
        return login()
        
    def regForm(self):
        register = form.Form(form.Textbox('username'),
                             form.Password('password'),
                             form.Password('password_again'),
                             validators = [form.Validator("Las contrasenas no coinciden.", lambda i: i.password == i.password_again),
                                           form.Validator("El nombre de usuario seleccionado ya existe", lambda i: not session['usr'].checkUsername(i.username))])
        return register()

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
