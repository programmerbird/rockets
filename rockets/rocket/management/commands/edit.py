#!/usr/bin/env python
#-*- coding:utf-8 -*-


from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
from rockets import models
from rockets import loaders



class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		if not args:
			services = loaders.list_services()
			services.sort()
			for service in services:
				self.stdout.write(service)
		else:
			app_name = args[0]
			app_args = args[1:]
			try:
				self.stdout.write("Editing %s ...\n" % app_name)
				n = loaders.get_service(app_name)()
				n.command = self
				n.console.command = self
				n.node = models.Node.current()
				n.load(*app_args)
				n.edit(*app_args)
			except Exception, e:
				raise CommandError(unicode(e))

