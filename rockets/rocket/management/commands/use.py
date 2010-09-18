#!/usr/bin/env python
#-*- coding:utf-8 -*-


from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
from rockets.rocket.models import *
from rockets.rocket.loaders import list_services, get_service


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
					self.stdout.write("%s [selected]\n" % node.name)
				else:
					self.stdout.write("%s\n" % node.name)
		else:
			node_name = args[0]
			try:
				node = Node.objects.get(name=node_name)
			except Node.DoesNotExist:
				raise CommandError('Node "%s" does not exist' % node_name)
			Session.store('node', node.name)
			
