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
				self.stdout.write("%s\n" % service)
		else:
			app_name = args[0]
			app_args = args[1:]
			try:
				self.stdout.write("Adding %s ...\n" % app_name)
				n = loaders.get_service(app_name)()
				n.command = self
				n.console.command = self
				n.node = models.Node.current()
				n.init(*app_args)
				n.add(*app_args)
			except KeyboardInterrupt:
				self.stdout.write("\nGoodbye :)\n")
			except Exception, e:
				import traceback
				traceback.print_exc()
				raise CommandError(unicode(e))

