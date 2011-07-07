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
		env.host_string = '%(user)s@%(public_ip)s' % locals()
		local('ssh -p %(port)s %(host_string)s' % env, capture=False)

