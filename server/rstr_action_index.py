#!/usr/bin/env python

import web

render = web.ctx.session['render']
usr = web.ctx.session['usr']

class index:
    def GET(self):
        blocks = [render.login(usr.loginForm())]
        left = render.left(blocks)
        center = render.center()
        right = render.right()
        return render.index(left, center, right, "Ritho's streaming", "static/style.css", "static/jquery.js", "")
    def POST(self):
        left = render.left({})
        center = render.center()
        right = render.right()
        return render.index(left, center, right, "Ritho's streaming", "static/style.css", "static/jquery.js", "")
