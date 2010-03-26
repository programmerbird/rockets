#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
from django.db.models.query_utils import CollectedObjects
from django import forms
from servers.console import menu, new_form, edit_form
from servers.models import *


Model = Provider

class UsageError(CommandError):
	def __init__(self, txt):
		super(UsageError, self).__init__("Usage: boatyard provider " + txt)

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
		
		provider = obj 
		form = DRIVERS_MAP[provider.driver](data=json.loads(provider.storage))
		form = edit_form(form)
		provider.storage = json.dumps(form.data)
		provider.save()
		
	def add(self, *args, **kwargs):
		if len(args)!=1:
			raise UsageError("add <name>")
			
		name = args[0]
		if Model.objects.filter(name=name):
			raise CommandError("[%s] alread existed" % name)
			
		print "Please select driver below:"
		form = menu([
			(x(), x.Meta.slug) for x in DRIVERS 
		])
		form = new_form(form)
		p = Provider()
		p.name = name 
		p.driver = getattr(types, form.Meta.slug)
		p.storage = json.dumps(form.data)
		p.save()
		
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

