#!/usr/bin/env python
# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

import web

render = web.ctx.session['render']
usr = web.ctx.session['usr']

class Index:
    def GET(self):
        blocks = [render.login(usr.loginForm())]
        left = render.left(blocks)
        center = render.center()
        right = render.right()
        return render.index(left, center, right, "Ritho's streaming", "static/style.css", "static/jquery.js", "static/javascript.js")
    def POST(self):
        left = render.left({})
        center = render.center()
        right = render.right()
        return render.index(left, center, right, "Ritho's streaming", "static/style.css", "static/jquery.js", "static/javascript.js")
