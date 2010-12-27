#!/usr/bin/env python
#-*- coding:utf-8 -*-


from django.core.management import setup_environ
try:
	import settings # Assumed to be in the same directory.
except ImportError:
	import sys
	sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
	sys.exit(1)

if __name__ == "__main__":
	setup_environ(settings)
	import os, sys, getpass
	from core.templates import dump
	
	project_path = sys.argv[1]
	user = getpass.getuser()
	prototype_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'prototype'))
	dump(prototype_path, project_path, {
		'secret': unicode(os.urandom(32).encode('hex')),
		'user': unicode(user),
	})

