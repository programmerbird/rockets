#-*- coding:utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from rockets.servers.models import Node
from rockets.servers.utils import get_service
from django.utils import simplejson

import sys
class UsageError(CommandError):
	def __init__(self, txt):
		super(UsageError, self).__init__("Usage: boatyard install " + txt)


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		if len(args)!=1:
			raise UsageError("<service name>")
		
		from rockets.servers.api import connect
		connect()
		name = args[0]
		node = Node.current()
		print node
		if name in node.get_services():
			print "[%s] already installed" % name 
			return 
			
		service = get_service(name)
		service.install(*args[1:])
		
		node.get_services().append(name)
		node.save()
		
		print "[%s] installed" % name
		
		sys.exit(0)
		

