#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys 
import os 
import getpass
from rockets.servers.path import clone 

def main(*args):
	path = args[0]
	user = getpass().getuser()
	prototype_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../prototype/'))
	clone(prototype_path, path, {
		'secret': os.urandom(8).encode('hex'),
		'user': user,
	})

if __name__ == '__main__':
	sys.exit(main())

