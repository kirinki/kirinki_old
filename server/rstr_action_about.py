#!/usr/bin/env python

import web

render = web.ctx.session['render']

class about:
    def GET(self):
        # blocks = [render.login(user.loginForm()), render.section(render.article("Title","abstract","content"))]
        # left = render.left(blocks)
        left = render.left({})
        center = render.center()
        right = render.right()
        return render.index(left, center, right, "Ritho's streaming", "static/style.css", "static/jquery.js", "")
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
        return render.index(left, center, right, "Ritho's streaming", "static/style.css", "static/jquery.js", "")
