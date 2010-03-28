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
	prototype_path = os.path.join(sys.prefix, 'rockets', 'prototype')
	clone(prototype_path, path, {
		'secret': os.urandom(8).encode('hex'),
		'user': user,
	})
	open(os.path.join(path, '__init__.py'), 'w').close()

if __name__ == '__main__':
	sys.exit(main())

