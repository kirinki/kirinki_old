import os
import sys
sys.path.append('/var/www/')
sys.path.append('/var/www/kirinki')
os.environ['DJANGO_SETTINGS_MODULE'] = 'kirinki.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
