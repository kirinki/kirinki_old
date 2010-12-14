import os
import sys
sys.path.append('/home/i02sopop/desarrollo/rstreaming/django')
sys.path.append('/home/i02sopop/desarrollo/rstreaming/django/rstreaming')
os.environ['DJANGO_SETTINGS_MODULE'] = 'rstreaming.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
