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
packages, package_paths = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
	os.chdir(root_dir)
rockets_dir = 'rockets'

for dirpath, dirnames, filenames in os.walk(rockets_dir):
	# Ignore dirnames that start with '.'
	for i, dirname in enumerate(dirnames):
		if dirname.startswith('.'): del dirnames[i]
	if '__init__.py' in filenames:
		package = '.'.join(fullsplit(dirpath))
		packages.append(package)
	elif filenames:
		package_paths.append(dirpath)
		
def find_package(dirpath):
	chunks = fullsplit(dirpath)
	while chunks:
		package = '.'.join(chunks)
		if package in packages:
			return package
		chunks = chunks[:-1]
		
package_data = {}
for x in package_paths:
	package = find_package(x)
	if not package in package_data:
		package_data[package] = []
	package_data[package].append( x[len(package)+1:] + '/*' )


print package_data
	
VERSION = __import__('rockets').VERSION
try:
	setup(name='Rockets',
		version=VERSION,
		description='Server management tools',
		author='Sittipon Simasanti',
		author_email='ssimasanti@gmail.com',
		url='http://github.com/ssimasanti/rockets/',
		scripts=['rockets/bin/rocket',],
		requires=[
			'Django (>=1.2.3)',
		],
		packages=packages,
		package_data = package_data,
		)
except:
	import traceback
	traceback.print_exc()

