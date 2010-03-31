#-*- coding:utf-8 -*-

from fabric.api import *
from fabric.contrib.files import exists, append
from django.conf import settings 
from rockets.servers.models import Node 
from rockets.servers.console import menu
from utils import ServerManagementUtility

def manage(txt):
	args = txt
	if isinstance(args, basestring):
		args = args.split(' ')
	args = ['manage.py'] + args
	utility = ServerManagementUtility(args)
	utility.execute()
	

def connect():
	node = Node.current()
	env.node = node 
	env.user = node.username 
	env.password = node.get_password()
	env.host = node.get_public_ip()[0]
	env.host_string = '%s@%s' % (env.user, env.host)
	if env.user=='root':
		env.home = '/root'
	else:
		env.home = '/home/%s' % env.user 
	try:
		local('grep "%(host)s" ~/.ssh/known_hosts' % env)
	except:
		local('ssh-keyscan -t rsa "%(host)s" >> ~/.ssh/known_hosts' % env)
	


