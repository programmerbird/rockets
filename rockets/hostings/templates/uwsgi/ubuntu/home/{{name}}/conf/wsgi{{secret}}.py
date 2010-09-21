import os,sys

sys.path.append('/home/{{name}}/uwsgi/app{{secret}}/')
sys.path.append('/home/{{name}}/uwsgi/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'app{{secret}}.{{django_settings}}'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

