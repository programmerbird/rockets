#-*- coding:utf-8 -*-
"""
Install SSH Public Key

usage: 

boatyard authorized_keys add [keyname] to [username] 
boatyard authorized_keys add [keyname] // username==keyname

"""
from rockets.servers.api import *
from rockets.keys.models import PublicKey
		
def add(*args):
	if len(args) not in (1,3):
		raise AttributeError
	keyname = args[0]
	env.keyuser = args[-1]
	
	publickey = PublicKey.objects.get(name=keyname)
	if env.keyuser=='root':
		env.keyhome = '/root'
	else:
		env.keyhome = '/home/%s' % env.keyuser

	if not exists(env.keyhome):
		raise Exception("User [%s] does not exists" % env.keyuser)
		
	run('mkdir -p %(keyhome)s/.ssh' % env, pty=True)
	
	keys = publickey.content.split('\n')
	append(keys, '%(keyhome)s/.ssh/authorized_keys' % env)
	
	run('chown -R %(keyuser)s:%(keyuser)s %(keyhome)s/.ssh/' % env, pty=True)
	print "authorized_keys added"

