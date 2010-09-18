#!/usr/bin/env python
#-*- coding:utf-8 -*-


from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
from rockets.models import *
from rockets.loaders import list_services, get_service


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
				n = get_service(app_name)()
				n.command = self
				n.node = Node.current()
				n.load(*service_args, **kwargs)
				n.edit(*service_args, **kwargs)
			except Exception, e:
				raise CommandError(unicode(e))

