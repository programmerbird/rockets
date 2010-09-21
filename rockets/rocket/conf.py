#!/usr/bin/env python
#-*- coding:utf-8 -*-


from django.conf import settings

SERVER_DUMP_PATH = getattr(settings, 'SERVER_DUMP_PATH', '/tmp')
SAVE_CONFIRMATION = getattr(settings, 'SAVE_CONFIRMATION', False)
DELETE_CONFIRMATION = getattr(settings, 'DELETE_CONFIRMATION', True)
