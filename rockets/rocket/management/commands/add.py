#!/usr/bin/env python
#-*- coding:utf-8 -*-


from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
from rockets.rocket.models import *
from rockets.rocket.loaders import list_services, get_service


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		if not args:
			services = list_services()
			services.sort()
			for service in services:
				self.stdout.write("%s\n" % service)
		else:
			app_name = args[0]
			app_args = args[1:]
			try:
				self.stdout.write("Adding %s ...\n" % app_name)
				n = get_service(app_name)()
				n.command = self
				n.console.command = self
				n.node = Node.current()
				n.add(*app_args, **kwargs)
			except KeyboardInterrupt:
				self.stdout.write("\nSee ya :)\n")
			except Exception, e:
				raise CommandError(unicode(e))

