#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
from django.db.models.query_utils import CollectedObjects
from rockets.servers.utils import get_service, get_services
from rockets.servers.models import Node
from rockets.servers.conf import session 

import os 
from fabric.api import *

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		node = Node.current()
		
		password = node.password or os.urandom(8).encode('hex')
		if not '--random' in args:
			node.password = prompt('New Password', default=password)
		node.set_password(node.password)
		node.save()

