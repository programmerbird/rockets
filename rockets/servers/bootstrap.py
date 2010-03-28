#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys 
import os 
import getpass

from django.core.management import setup_environ
import settings
setup_environ(settings)

from path import clone

def main():
	
	path = sys.argv[1]
	user = getpass.getuser()
	prototype_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../prototype'))
	clone(prototype_path, path, {
		'secret': unicode(os.urandom(32).encode('hex')),
		'user': unicode(user),
	})
	open(os.path.join(path, '__init__.py'), 'w').close()

if __name__ == '__main__':
	sys.exit(main())

