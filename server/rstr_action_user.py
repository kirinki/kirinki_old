#!/usr/bin/env python

import web

render = web.ctx.session['render']

class User:
    def GET(self):
        # blocks = [render.login(usr.login()), render.section(render.article("Title","abstract","content"))]
        # left = render.left(blocks)
        left = render.left({})
        center = render.center()
        right = render.right()
        return render.index(left, center, right, "Ritho's streaming", "static/style.css", "static/jquery.js", "static/javascript.js")
    def POST(self):
        #if not usr.login().validates(): 
        #    blocks = [render.login(form)]
        #else:
        #    blocks = ["Grrreat success! %s is login" % (form['username'].value)]
        #blocks.append(render.section(render.article("Title","abstract","content")))
        #left = render.left(blocks)
        left = render.left({})
        center = render.center()
        right = render.right()
        return render.index(left, center, right, "Ritho's streaming", "static/style.css", "static/jquery.js", "static/javascript.js")
