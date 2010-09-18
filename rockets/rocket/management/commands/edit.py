#!/usr/bin/env python
#-*- coding:utf-8 -*-


from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
from rocket.models import *
from rocket.loaders import list_services, get_service



class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		if not args:
			services = list_services()
			services.sort()
			for service in services:
				self.stdout.write(service)
		else:
			app_name = args[0]
			app_args = args[1:]
			try:
				self.stdout.write("Editing %s ...\n" % app_name)
				n = get_service(app_name)()
				n.command = self
				n.console.command = self
				n.node = Node.current()
				n.load(*app_args, **kwargs)
				n.edit(*app_args, **kwargs)
			except Exception, e:
				raise CommandError(unicode(e))

