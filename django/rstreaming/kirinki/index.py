# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

# Django imports
from django.contrib import messages
from django.template import RequestContext
from django.template.loader import render_to_string

# Application imports
from kirinki.user import LoginForm
from kirinki.config import Config
from kirinki.mainviewer import MainViewer

class IndexController():
    '''Class to implement the Index controller'''
    def __init__(self, request):
        #request.session.clear()
        if request.session.get('isConfig', False) is False:
            Config.getSession(request.session)
        leftBlocks = []
        if not request.session['user'].is_authenticated():
            leftBlocks = [render_to_string('kirinki/section.html', {'title' : 'login', 'content': render_to_string('kirinki/form.html', {'form' : LoginForm(), 'action' : request.session['base_url']+'/login'}, context_instance=RequestContext(request))})]
        centerBlocks = [render_to_string('kirinki/section.html', {'title' : 'Bienvenido', 'content' : '<p>Bienvenido a Ritho\'s Streaming, el sitio desde el cual podras hacer Streaming tanto en directo como en diferido de manera sencilla.</p>'})]
        rightBlocks = [self.generateArticles(), self.generateVideos()]
        self.render = MainViewer(request).render(leftBlocks, centerBlocks, rightBlocks)

    def generateArticles(self):
        # article = render_to_string('kirinki/article.html', {'title' : 'Inicio del proyecto', 'date' : '2010-12-01','abstract' : 'Con la inauguracion de esta oficial comienza su andadura el proyecto.', 'content' : 'Explicacion del proyecto RStreaming'})
        # return render_to_string('kirinki/section.html', {'title' : 'Ultimas noticias', 'content' : article})
        return ''

    def generateVideos(self):
        # videos = render_to_string('kirinki/video.html', {'width' : '320', 'height' : '240', 'controls' : True, 'src': 'file:///home/i02sopop/Downloads/PiTP - 2009 - Monday, July 13, 2009 - Kernighan.hi.mp4'})
        # return render_to_string('kirinki/section.html', {'title' : 'Videos', 'content' : videos})
        return ''


    def getRender(self):
        return self.render

# $refer = $_SERVER["HTTP_REFERER"];
# if (strpos($refer,"google")) {
# $refer_string = parse_url($refer, PHP_URL_QUERY);
# parse_str($refer_string, $vars);
# $search_term = $vars['q'];
# $rank = $vars['cd'];
# $site_url = $vars['url'];

# $stmt = $db->prepare("INSERT INTO google_search_log VALUES (:search_term, :rank, :site_url, :results_url)");
# $stmt->bindParam(':search_term', $search_term);
# $stmt->bindParam(':rank', $rank);
# $stmt->bindParam(':site_url', $site_url);
# $stmt->bindParam(':results_url', 'http://www.google.com/search?q='.urlencode($search_term));
# $stmt->execute();
# }
