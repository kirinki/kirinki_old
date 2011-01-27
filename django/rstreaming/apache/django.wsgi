import os
import sys
sys.path.append('/usr/src/rstreaming/django')
sys.path.append('/usr/src/rstreaming/django/rstreaming')
os.environ['DJANGO_SETTINGS_MODULE'] = 'rstreaming.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
