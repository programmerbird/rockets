#-*- coding:utf-8 -*-

import os
from rockets.servers.api import *
from rockets.servers.path import get_server_dump_path
from fabric.contrib.console import confirm

def main(*args):
	path = get_server_dump_path(env.node)
	if os.path.exists(path):
		if confirm('Are you sure you want to clean %s?' % env.node.name):
			local('rm -rf %s/*' % path)

def scripts(*args):
	
	script_path = get_server_dump_path(env.node, 'SCRIPTS')
	if os.path.exists(script_path):
		if confirm('Are you sure you want to clean %s?' % env.node.name):
			local('rm -rf %s/*' % script_path)

