#!/usr/bin/env python

from web import form

class user:
    """User class"""
    def __init__(self):
        register = form.Form(form.Textbox('username'),
                             form.Password('password'),
                             form.Password('password_again'),
                             validators = [form.Validator("Las contrasenas no coinciden.", lambda i: i.password == i.password_again)])
    #form.Validator("El nombre de usuario seleccionado ya existe", lambda i: !session['usr'].checkUsername(i.username))])
    
        login = form.Form(form.Textbox('username'),
                          form.Password('password'))
                      #validators = [form.Validator("Usuario o contrasena incorrectos.", lambda i: session['usr'].login(i))])

        self.reg = register()
        self.log = login()
