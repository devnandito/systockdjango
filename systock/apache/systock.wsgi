import os
import sys
sys.path = ['/var/www/html/systock'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'systock.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
