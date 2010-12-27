#!/usr/bin/env python
#-*- coding:utf-8 -*-


from setuptools import setup, find_packages

VERSION = __import__('rockets').VERSION


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
	include_package_data=True,
	packages = find_packages(exclude=['ez_setup', 'tests', 'tests.*']),
	package_data = {
		'': [
			'*.sh', '*.html', '*.conf', '*}}', '*.list', 'rocket', '*rm', '*inst',
			'*.json', '*.list', '*.log', '*->',
		],
	},
)

