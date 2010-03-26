#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
from django.db.models.query_utils import CollectedObjects
from django import forms
from servers.console import menu, new_form, edit_form
from keys.models import *


Model = PublicKey

class UsageError(CommandError):
	def __init__(self, txt):
		super(UsageError, self).__init__("Usage: boatyard publickey " + txt)

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		if args:
			cmd = args[0]
			if cmd in ('add', 'mv', 'rm',):
				return getattr(self, cmd)(*args[1:])
				
		if not args:
			for x in Model.objects.all().order_by('name'):
				print unicode(x)
			return 
		
		name = args[0] 
		obj = Model.objects.get(name=name)
		print obj.content


	def add(self, *args, **kwargs):
		if len(args)!=1:
			raise UsageError("add <name> < ~/.ssh/id_rsa.pub")

		name = args[0]
		if Model.objects.filter(name=name):
			raise CommandError("[%s] alread existed" % name)

		import sys 
		content = ''.join(sys.stdin.readlines())
		if content:
			n = PublicKey()
			n.name = name 
			n.content = content 
			n.save()
		else:
			raise CommandError("no key specific")
					
	def mv(self, *args, **kwargs):
		if len(args) != 2:
			raise UsageError("mv <name> <newname>")
			
		name = args[0]
		new_name = args[1]
		
		try:
			obj = Model.objects.get(name=name)
		except Model.DoesNotExist:
			raise CommandError("[%s] does not exists" % name)
		if Model.objects.filter(name=new_name):
			raise CommandError("[%s] alread existed" % new_name)
		obj.name = new_name
		obj.save()
		
		
	def rm(self, *args, **kwargs):
		if len(args) != 1:
			raise UsageError("rm <name>")
			
		name = args[0]
		try:
			obj = Model.objects.get(name=name)
		except Model.DoesNotExist:
			raise CommandError("[%s] does not exists" % name)
		obj.delete()



