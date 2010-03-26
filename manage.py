#!/usr/bin/env python
import sys
from django.core.management import setup_environ
try:
	import settings # Assumed to be in the same directory.
except ImportError:
	sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
	sys.exit(1)

if __name__ == "__main__":
	setup_environ(settings)
	try:
		from servers.utils import ServerManagementUtility
		utility = ServerManagementUtility()
		utility.execute()
	except Exception, e:	
		print e
		sys.exit(1)
	sys.exit(0)

