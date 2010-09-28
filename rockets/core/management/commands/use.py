#!/usr/bin/env python
#-*- coding:utf-8 -*-


from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
from rockets.core import models
from rockets.core import loaders

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		if not args:
			try:
				selected_node = models.Node.current()
			except NoNodeSelected:
				selected_node = None
			nodes = models.Node.objects.all().order_by('name')
			for node in nodes:
				if node == selected_node:
					self.stdout.write("%s [selected]\n" % node.name)
				else:
					self.stdout.write("%s\n" % node.name)
		else:
			node_name = args[0]
			try:
				node = models.Node.objects.get(name=node_name)
			except models.Node.DoesNotExist:
				raise CommandError('Node "%s" does not exist' % node_name)
			models.Session.store('node', node.name)
			
