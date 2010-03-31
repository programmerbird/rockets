#-*- coding:utf-8 -*-
"""

"""
import os 
import random
from fabric.contrib.project import rsync_project
from rockets.servers.api import *
from rockets.servers.template import get_server_dump_path


def _scp_dir(local_dir=None, remote_dir=None, exclude=[]):
	print "[%(host_string)s] upload:" % env, local_dir, "->", remote_dir
	with hide('running', 'stdout'):
		try:
			secret = env.secret
			local('cd "%(local_dir)s"; tar -cvzf /tmp/deploy-%(secret)s.tar.gz *' % locals())
			put('/tmp/deploy-%(secret)s.tar.gz' % env, '/tmp/deploy-%(secret)s.tar.gz' % env)
			run('tar -xzf /tmp/deploy-%(secret)s.tar.gz --directory=%(remote_dir)s' % locals(), pty=True)
		finally:
			local('rm /tmp/deploy-%(secret)s.tar.gz' % env)
			run('rm /tmp/deploy-%(secret)s.tar.gz' % env, pty=True)


def _rsync_dir(local_dir=None, remote_dir=None, exclude=[]):
	try:
		return rsync_project(remote_dir, local_dir=os.path.join(local_dir, '*'), exclude=exclude, delete=False)
	except:
		return _scp_dir(local_dir=local_dir, remote_dir=remote_dir, exclude=exclude)

def _manage_upload_method(node, *args):
	storage = node.get_service_storage('push')
	if '--rsync' in args:
		storage['method'] = 'rsync'
		node.save() 
	if '--scp' in args:
		storage['method'] = 'scp' 
		node.save() 
	return storage.get('method', 'scp')

def _run_scripts(node):
	script_dir = get_server_dump_path(node, 'SCRIPTS')
	if not os.path.exists(script_dir):
		return
	try:
		with hide('running', 'stdout'):
			run('chmod +x /SCRIPTS/*', pty=True)
			scripts = os.listdir(script_dir)
			scripts.sort()
			for s in scripts:
				script_path = os.path.join(script_dir, s)
				if not os.path.isfile(script_path):
					continue
				if script_path.endswith('~'):
					continue
				print "[%(host_string)s] run:" % env, s
				remote_path = '/SCRIPTS/%s' % s 
				with show('stdout'):
					run(remote_path, pty=True)
				os.remove(script_path)
	finally:
		print "[%(host_string)s] clean" % env
		with hide('running', 'stdout', 'stderr'):
			for s in os.listdir(script_dir):
				remote_path = '/SCRIPTS/%s' % s 
				run('rm -f %s' % remote_path, pty=True)
			run('rmdir --ignore-fail-on-non-empty /SCRIPTS' % env, pty=True)
			try:
				os.rmdir(script_dir)
			except OSError:
				pass 

def main(*args):
	node = env.node
	method = _manage_upload_method(node, *args)

	env.upload_dir = _upload_dir = _rsync_dir if method=='rsync' else _scp_dir
	env.secret = os.urandom(8).encode('hex')

	path = get_server_dump_path(node)
	script_dir = get_server_dump_path(node, 'SCRIPTS')
	
	if os.path.exists(path):
		_upload_dir(path, '/')
	if os.path.exists(script_dir):
		_run_scripts(node)

