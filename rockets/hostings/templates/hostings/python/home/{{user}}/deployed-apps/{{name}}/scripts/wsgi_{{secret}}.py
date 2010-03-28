import os,sys

sys.path.append('/home/{{user}}/deployed-apps/{{name}}/app{{secret}}/')
sys.path.append('/home/{{user}}/deployed-apps/{{name}}/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'app{{secret}}.{{options.django_settings}}'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

