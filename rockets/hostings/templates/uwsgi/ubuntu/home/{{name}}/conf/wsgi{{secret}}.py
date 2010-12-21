#!/usr/bin/env python
#-*- coding:utf-8 -*-


import os,sys

sys.path.append('/home/{{name}}/app/uwsgi{{secret}}')
sys.path.append('/home/{{name}}/app')

os.environ['DJANGO_SETTINGS_MODULE'] = 'uwsgi{{secret}}.{{django_settings}}'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

