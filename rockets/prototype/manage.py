#!/usr/bin/env python
import sys
import os 

try:
	import settings # Assumed to be in the same directory.
except ImportError:
	sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
	sys.exit(1)

if __name__ == "__main__":
	from django.core.management import setup_environ
	setup_environ(settings)
	from rockets.servers.utils import execute_from_command
	execute_from_command()

