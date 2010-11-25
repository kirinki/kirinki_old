#!/usr/bin/env python
# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

import web

render = web.ctx.session['render']

class Register:
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
