#-*- coding:utf-8 -*-
"""
Install SSH Public Key

usage: 

rockets node [nodename] authorized_keys add [keyname] to [username] 
rockets node [nodename] authorized_keys add [keyname] // username==keyname

"""
from rockets.servers.api import *
from rockets.keys.models import PublicKey

ADMIN_USER = getattr(settings, 'ADMIN_USER', 'root')
ADMIN_PUBLICKEY_NAME = getattr(settings, 'ADMIN_PUBLICKEY_NAME', ADMIN_USER)

def install(*args):
	env.admin_user = ADMIN_USER
	env.public_key = ADMIN_PUBLICKEY_NAME
	try:
		manage("authorized_keys add %(public_key)s to %(user)s" % env)
		manage("authorized_keys add %(public_key)s to %(admin_user)s" % env)
	except:
		pass
		
	print "Adding Boatyard Repository.."
	append('deb http://boatyard.s3.amazonaws.com/packages/ubuntu karmic main', '/etc/apt/sources.list.d/x10studio.list')
	run('gpg --keyserver keyserver.ubuntu.com --recv-keys 9CE8C487', pty=True)
	run('gpg -a --export 9CE8C487 | sudo apt-key add -', pty=True)
	
	print "Updating server.."
	run('aptitude update', pty=True)
	
