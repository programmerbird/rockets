#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand
from django.db.models.query_utils import CollectedObjects
from django import forms
from servers.console import menu, new_form, edit_form
from servers.models import Provider, Node
from fabric.api import *

Model = Node
class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		if args:
			cmd = args[0]
			if cmd in ('rm',):
				return getattr(self, cmd)(*args[1:])
				
		nodes = []
		providers = Provider.objects.all()
		for provider in providers:
			for node in provider.get_driver().list_nodes():
				Node.get(provider, node.name)
				
		nodes = Node.objects.order_by('name')
		for node in nodes:
			print node
		return 

	def rm(self, *args, **kwargs):
		if len(args) != 1:
			raise UsageError("rm <name>")
			
		name = args[0]
		try:
			obj = Model.objects.get(name=name)
		except Model.DoesNotExist:
			raise CommandError("[%s] does not exists" % name)
		obj.delete()
	
		

	
