#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os 
import json 

from fabric.api import put, run, local, cd, settings, env, hide, show
from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
from rockets import models
from rockets import loaders
from rockets import conf 

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		node = models.Node.current()
		
		public_ip = json.loads(node.public_ip or "[]")[0]
		env.hosts = [public_ip]
		env.user = user = node.username
		env.port = port = node.port 
		env.bundle = bundle = models.Session.bundle()
		env.secret = secret = os.urandom(5).encode('hex')
		env.secret2 = secret2 = os.urandom(5).encode('hex')
		env.host_string = '%(user)s@%(public_ip)s:%(port)s' % locals()
		
		dump_path = os.path.join(conf.SERVER_DUMP_PATH, node.name)
		script_path = os.path.join(conf.SERVER_DUMP_PATH, node.name, 'SCRIPTS') 
		bundle_path = '/tmp/rocket-%(bundle)s' % env 
		bundle_script_path = os.path.join(bundle_path, 'SCRIPTS')
		
		scripts = [ x for x in os.listdir(script_path) if not x.endswith('~') ]
		scripts.sort()
		try:
			with cd(dump_path):
				local('tar czf /tmp/rocket-%(secret)s.tar.gz *' % locals(), capture=False)
				put('/tmp/rocket-%(secret)s.tar.gz' % env, '/tmp/rocket-%(secret2)s.tar.gz' % env)
				run('mkdir -p /tmp/rocket-%(bundle)s' % env, pty=True)
				run('tar xzf /tmp/rocket-%(secret2)s.tar.gz --no-overwrite-dir --directory=/tmp/rocket-%(bundle)s' % env, pty=True)
			
				if scripts:
					run('chmod +x %(bundle_path)s/SCRIPTS/*' % locals())
					for script in scripts:
						run('%(bundle_path)s/SCRIPTS/%(script)s' % locals(), pty=True)
						os.remove(os.path.join('SCRIPTS', script))
		finally:
			with hide('running', 'stdout', 'stderr'):
				run('rm -rf /tmp/rocket-%(secret2)s.tar.gz' % locals())
				run('rm -rf /tmp/rocket-%(bundle)s' % locals())
				local('rm -rf /tmp/rocket-%(secret)s*' % locals())
					 

