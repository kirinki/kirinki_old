#!/usr/bin/env python
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

import sys, os
abspath = '/home/i02sopop/desarrollo/rstreaming/server/'
sys.path.append(abspath)
os.chdir(abspath)

import web
from rstr_init import *

class index:
    def GET(self):
        # blocks = [render.login(user.login()), render.section(render.article("Title","abstract","content"))]
        # left = render.left(blocks)
        left = render.left({})
        center = render.center()
        right = render.right()
        return render.index(unicode(left), unicode(center), unicode(right), "Ritho's streaming", "static/style.css", "static/jquery.js", "")
    def POST(self):
        #if not user.login().validates(): 
        #    blocks = [render.login(form)]
        #else:
        #    blocks = ["Grrreat success! %s is login" % (form['username'].value)]
        #blocks.append(render.section(render.article("Title","abstract","content")))
        #left = render.left(blocks)
        left = render.left({})
        center = render.center()
        right = render.right()
        return render.index(unicode(left), unicode(center), unicode(right), "Ritho's streaming", "static/style.css", "static/jquery.js", "")

class about:
    def GET(self):
        #form = login()
        #blocks = [render.login(form), render.section(render.article("Title","abstract","content"))]
        #left = render.left(blocks)
        left = render.left({})
        center = render.center()
        right = render.right()
        return render.index(unicode(left), unicode(center), unicode(right), "Ritho's streaming", "static/style.css", "static/jquery.js", "")
    def POST(self):
        #form = login()
        #if not form.validates(): 
        #    blocks = [render.login(form)]
        #else:
        #    blocks = ["Grrreat success! %s is login" % (form['username'].value)]
        #blocks.append(render.section(render.article("Title","abstract","content")))
        #left = render.left(blocks)
        left = render.left({})
        center = render.center()
        right = render.right()
        return render.index(unicode(left), unicode(center), unicode(right), "Ritho's streaming", "static/style.css", "static/jquery.js", "")

application = web.application(urls, globals()).wsgifunc()

# db = web.database(dbn='postgres', user='username', pw='password', db='dbname')
# todos = db.select('todo')
# return render.index(todos)
# post_data=web.input(name=[])
# n = db.insert('todo', title=data.title)
# raise web.seeother('/'+data.name)
