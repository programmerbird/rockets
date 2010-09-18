#!/usr/bin/env python
#-*- coding:utf-8 -*-


from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
from rockets.models import *

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		if not args:
			try:
				selected_node = Node.current()
			except NoNodeSelected:
				selected_node = None
			nodes = Node.objects.all().order_by('name')
			for node in nodes:
				if node == selected_node:
					self.stdout.write("%s (selected)" % node.name)
				else:
					self.stdout.write(node.name)
		else:
			node_name = args[0]
			try:
				node = Node.objects.get(name=node_name)
			except Node.DoesNotExist:
				raise CommandError('Node "%s" does not exist' % node_name)
			Session.set('node', node.name)
			
