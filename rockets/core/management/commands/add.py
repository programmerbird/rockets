#!/usr/bin/env python
#-*- coding:utf-8 -*-


from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
from rockets.core import models
from rockets.core import loaders


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		if not args:
			services = loaders.list_services()
			services.sort()
			for service in services:
				self.stdout.write("%s\n" % service)
		else:
			app_kind = args[0]
			app_name = args[1]
			app_args = args[2:]
			try:
				self.stdout.write("Adding %s ...\n" % app_kind)
				pk = '%s:%s' % (app_kind, app_name) 
				node = models.Node.current()
				service, is_created = node.get_or_create_service(pk)
				service.io(self)
				service.add(*app_args)
			except KeyboardInterrupt:
				self.stdout.write("\nGoodbye :)\n")
			except Exception, e:
				import traceback
				traceback.print_exc()
				raise CommandError(unicode(e))

