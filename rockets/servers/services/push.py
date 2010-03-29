#-*- coding:utf-8 -*-
"""

"""
import os 
import random
from fabric.contrib.project import rsync_project
from rockets.servers.api import *
from rockets.servers.template import get_server_dump_path

def get_required_dirs(local_dir, exclude=[]):
	result_dirs = []
	for local_path, dirs, files in os.walk(local_dir):
		if local_path in exclude:
			continue
		result_dirs.append(local_path)
		for name in dirs:
			path = os.path.join(local_path, name)
			if path in exclude:
				continue
			result_dirs.append(path)
			
	result_dirs.sort(cmp=lambda a,b: cmp(len(a), len(b)), reverse=True)
	created_dirs = []
	for x in result_dirs:
		has = False
		for a in created_dirs:
			if a.startswith(x):
				has = True 
				break
		if not has:
			created_dirs.append(x)
	created_dirs.sort()
	return created_dirs
	
def sync(remote, local_dir=None, exclude=[], delete=False):
	try:
		return rsync_project('/', local_dir=os.path.join(local_dir, '*'), exclude=exclude, delete=delete)
	except:
		dirs = get_required_dirs(local_dir, exclude=exclude)
		for local_path in dirs:
			remote_path = os.path.join(remote, local_path[len(local_dir)+1:])
			run('mkdir -p "%s"' % remote_path, pty=True)
		
		for local_path, dirs, files in os.walk(local_dir):
			if local_path in exclude:
				continue
			remote_path = os.path.join(remote, local_path[len(local_dir)+1:])
			for name in files:
				local_name = os.path.join(local_path, name)
				if local_name in exclude:
					continue
				remote_name = os.path.join(remote_path, name)
				put(local_name, remote_name)
			
def main(*args):
	node = env.node
	path = get_server_dump_path(node)
	script_dir = get_server_dump_path(node, 'SCRIPTS')
	
	sync('/', local_dir=path, exclude=[script_dir], delete=False)
	return 
	
	for s in os.listdir(script_dir):
		script_path = os.path.join(script_dir, s)
		if not os.path.isfile(script_path):
			continue
		if script_path.endswith('~'):
			continue
		remote_path = '/tmp/rockets-%s' % s 
		put(script_path, remote_path)
		run('chmod +x "%s"' % remote_path, pty=True)
		run(remote_path, pty=True)
		run('rm "%s"' % remote_path, pty=True)
		os.remove(script_path)
		
	try:
		os.rmdir(script_dir)
	except OSError:
		pass 
