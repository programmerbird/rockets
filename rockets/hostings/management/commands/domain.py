#-*- coding:utf-8 -*-

import os
from django import forms
from django.db.models.query_utils import CollectedObjects
from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
from django.conf import settings
from django.utils import simplejson as json
from rockets.servers.console import menu, new_form, edit_form
from rockets.servers.models import Node
from rockets.servers.path import clone
from rockets.servers.api import manage 
from rockets.hostings.models import Application, Alias, APPLICATIONS, APPLICATION_MAP


Model = Alias

SERVER_DUMP_PATH = getattr(settings, 'SERVER_DUMP_PATH')

class UsageError(CommandError):
	def __init__(self, txt):
		super(UsageError, self).__init__("Usage: rockets application " + txt)

class Command(BaseCommand):
	def handle(self, *args, **kwargs):

		if args:
			cmd = args[0]
			if cmd in ('add', 'rm',):
				return getattr(self, cmd)(*args[1:])
				
		node = Node.current()
		if not args:
			for x in Model.objects.filter(application__node=node).order_by('application__name', 'name'):
				print '%-40s' % unicode(x), unicode(x.application)
			return 
				
	def add(self, *args, **kwargs):
		if len(args)<2:
			raise UsageError("add <application> <domain>")
			
		node = Node.current()
		app_name = args[0]
		for name in args[1:]:
			try:
				application = Application.objects.get(name=app_name)
			except Application.DoesNotExist:
				raise CommandError("Unknown application [%s]" % app_name)
			if Model.objects.filter(application__node=node, name=name).exclude(application=application):
				raise CommandError("[%s] already existed" % name)
			
			Model.objects.get_or_create(application=application, name=name)	
		
		manage('application dump %s' % app_name)
		
	def rm(self, *args, **kwargs):
		if len(args) != 1:
			raise UsageError("rm <domain>")
		node = Node.current()
			
		name = args[0]
		try:
			obj = Model.objects.get(application__node=node, name=name)
		except Model.DoesNotExist:
			raise CommandError("[%s] does not exists" % name)
		obj.delete()

