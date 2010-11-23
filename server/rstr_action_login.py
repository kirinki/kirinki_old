#!/usr/bin/env python

import web

render = web.ctx.session['render']
usr = web.ctx.session['usr']

class Login:
    def GET(self):
        blocks = [render.login(usr.loginForm())]
        left = render.left(blocks)
        center = render.center()
        right = render.right()
        return render.index(left, center, right, "Ritho's streaming", "static/style.css", "static/jquery.js", "static/javascript.js")
    def POST(self):
        if not usr.loginForm().validates(): 
            blocks = [render.login(usr.lForm)]
        else:
            blocks = ["Grrreat success! %s is login" % (usr.lForm['username'].value)]
        #blocks.append(render.section(render.article("Title","abstract","content")))
        left = render.left(blocks)
        center = render.center()
        right = render.right()
        return render.index(left, center, right, "Ritho's streaming", "static/style.css", "static/jquery.js", "static/javascript.js")
