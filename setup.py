#!/usr/bin/env python
from distutils.core import setup
import os
import sys


def fullsplit(path, result=None):
	"""
	Split a pathname into components (the opposite of os.path.join) in a
	platform-neutral way.
	"""
	if result is None:
		result = []
	head, tail = os.path.split(path)
	if head == '':
		return [tail] + result
	if head == path:
		return result
	return fullsplit(head, [tail] + result)

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
	os.chdir(root_dir)
rockets_dir = 'rockets'

for dirpath, dirnames, filenames in os.walk(rockets_dir):
	# Ignore dirnames that start with '.'
	for i, dirname in enumerate(dirnames):
		if dirname.startswith('.'): del dirnames[i]
	if '__init__.py' in filenames:
		packages.append('.'.join(fullsplit(dirpath)))
	elif filenames:
		data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames if not f.endswith('~')]])

VERSION = __import__('rockets').VERSION

from distutils.core import setup

setup(name='Rockets',
	version=VERSION,
	description='Cloud management tools',
	author='Sittipon Simasanti',
	author_email='ssimasanti@gmail.com',
	url='http://github.com/ssimasanti/rockets/',
	scripts=['rockets/bin/rocket',],
	install_requires=[
		'Django>=1.1.1',
	],
	packages=packages,
	data_files=data_files,
	)
