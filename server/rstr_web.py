#!/usr/bin/env python

import os
import sys
import web
from web import form

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import rstr_config

web.config.debug = True
# /(.*)
urls = (
  '/', 'index',
  '/about', 'about'
)

app = web.application(urls, globals())
render = web.template.render('/home/i02sopop/desarrollo/rstreaming/server/templates/')

if web.config.debug:
    if web.config.get('_session') is None:
        db = web.database(dbn='postgres', db='rstreaming', user='i02sopop', pw='')
        store = web.session.DBStore(db, 'sessions')
        session = web.session.Session(app, store, {})
        web.config._session = session
    else:
        session = web.config._session
else:
    db = web.database(dbn='postgres', db='rstreaming', user='i02sopop', pw='')
    store = web.session.DBStore(db, 'sessions')
    session = web.session.Session(app, store, initializer={})

login = form.Form(form.Textbox('username'),
                  form.Password('password'),
                  form.Password('password_again'),
                  validators = [form.Validator("Las contrasenas no coinciden.", lambda i: i.password == i.password_again)])

class index:
    def GET(self):
        form = login()
        blocks = [render.login(form), render.section(render.article("Title","abstract","content"))]
        left = render.left(blocks)
        center = render.center()
        right = render.right()
        return render.index(unicode(left), unicode(center), unicode(right), "Ritho's streaming", "static/style.css", "static/jquery.js", "")
    def POST(self):
        form = login()
        if not form.validates(): 
            blocks = [render.login(form)]
        else:
            blocks = ["Grrreat success! %s is login" % (form['username'].value)]
        blocks.append(render.section(render.article("Title","abstract","content")))
        left = render.left(blocks)
        center = render.center()
        right = render.right()
        return render.index(unicode(left), unicode(center), unicode(right), "Ritho's streaming", "static/style.css", "static/jquery.js", "")

class about:
    def GET(self):
        form = login()
        blocks = [render.login(form), render.section(render.article("Title","abstract","content"))]
        left = render.left(blocks)
        center = render.center()
        right = render.right()
        return render.index(unicode(left), unicode(center), unicode(right), "Ritho's streaming", "static/style.css", "static/jquery.js", "")
    def POST(self):
        form = login()
        if not form.validates(): 
            blocks = [render.login(form)]
        else:
            blocks = ["Grrreat success! %s is login" % (form['username'].value)]
        blocks.append(render.section(render.article("Title","abstract","content")))
        left = render.left(blocks)
        center = render.center()
        right = render.right()
        return render.index(unicode(left), unicode(center), unicode(right), "Ritho's streaming", "static/style.css", "static/jquery.js", "")

# print config.strcfg

application = web.application(urls, globals()).wsgifunc()

# db = web.database(dbn='postgres', user='username', pw='password', db='dbname')
# todos = db.select('todo')
# return render.index(todos)
# globals = {}
# post_data=web.input(name=[])
# n = db.insert('todo', title=data.title)
# raise web.seeother('/'+data.name)
