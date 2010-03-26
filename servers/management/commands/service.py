#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
from django.db.models.query_utils import CollectedObjects
from servers.utils import get_service, get_services
from servers.models import Node
from servers.conf import session 

from fabric.api import *

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		node = Node.current()
		print node
		for x in node.get_services():
			print "-", x, "[installed]"
		
		for (service_name, path, options) in get_services():
			if options['NEED_INSTALLED']:
				continue
			print '-', service_name
		print ''
