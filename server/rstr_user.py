#!/usr/bin/env python

from web import form

class user:
    """User class"""
    def __init__(self):
        self.data = {'username' : '', 'password' : '', 'name' : '', 'surname' : '', 'videos' : [] }
        register = form.Form(form.Textbox('username'),
                             form.Password('password'),
                             form.Password('password_again'),
                             validators = [form.Validator("Las contrasenas no coinciden.", lambda i: i.password == i.password_again),
                                           form.Validator("El nombre de usuario seleccionado ya existe", lambda i: not session['usr'].checkUsername(i.username))])
    
        login = form.Form(form.Textbox('username'),
                          form.Password('password'),
                          validators = [form.Validator("Usuario o contrasena incorrectos.", lambda i: session['usr'].login(i))])

        self.reg = register()
        self.log = login()

    def checkUsername(self, user):
        return True

    def login(self, data):
        return True

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
