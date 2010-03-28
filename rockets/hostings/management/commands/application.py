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
from rockets.hostings.models import Application, APPLICATIONS, APPLICATION_MAP


Model = Application

SERVER_DUMP_PATH = getattr(settings, 'SERVER_DUMP_PATH')

class UsageError(CommandError):
	def __init__(self, txt):
		super(UsageError, self).__init__("Usage: rockets application " + txt)

class Command(BaseCommand):
	def handle(self, *args, **kwargs):

		if args:
			cmd = args[0]
			if cmd in ('add', 'mv', 'rm', 'dump',):
				return getattr(self, cmd)(*args[1:])
				
		node = Node.current()
		if not args:
			for x in Model.objects.filter(node=node).order_by('name'):
				print unicode(x)
			return 
		
		print node
		name = args[0] 
		obj = Model.objects.get(name=name, node=node)
		data=json.loads(obj.options)
		data['user'] = obj.user
		
		form_class = APPLICATION_MAP[obj.kind]
		class UserForm(form_class):
			user = forms.CharField()
		form = UserForm(data=data)
		form = edit_form(form)
		
		obj.node = node
		obj.kind = form.Meta.name
		obj.user = form.data['user']
		del form.data['user']
		obj.options = json.dumps(form.data)
		obj.save()
		
		manage('application dump %s' % name)
		
	def add(self, *args, **kwargs):
		if len(args)!=1:
			raise UsageError("add <name>")
			
		node = Node.current()
		name = args[0]
		if Model.objects.filter(node=node, name=name):
			raise CommandError("[%s] alread existed" % name)
			
		print "Please select driver below:"
		form_class = menu([
			(x, x.Meta.name) for x in APPLICATIONS 
		])
		class UserForm(form_class):
			user = forms.CharField()
		form = new_form(UserForm())
		p = Model()
		p.name = name 
		p.node = node
		p.kind = form.Meta.name
		p.user = form.data['user']
		del form.data['user']
		p.options = json.dumps(form.data)
		p.save()

		manage('application dump %s' % name)
		
	def dump(self, *args, **kwargs):
		if len(args)!=1:
			raise UsageError("dump <name>")
			
		name = args[0]
		node = Node.current()
		try:
			obj = Model.objects.get(node=node, name=name)
		except Model.DoesNotExist:
			raise CommandError("[%s] does not exists" % name)
			
		source = os.path.abspath(os.path.join(__file__, '../../../templates/hostings/%s/' % obj.kind))
		target = os.path.abspath(os.path.join(SERVER_DUMP_PATH, node.name))
		data = dict(obj.__dict__)
		data['application'] = obj
		data['options'] = obj.params
		clone(source, target, data)
			
		
	def mv(self, *args, **kwargs):
		if len(args) != 2:
			raise UsageError("mv <name> <newname>")
			
		name = args[0]
		new_name = args[1]
		
		node = Node.current()
		try:
			obj = Model.objects.get(node=node, name=name)
		except Model.DoesNotExist:
			raise CommandError("[%s] does not exists" % name)
		if Model.objects.filter(node=node, name=new_name):
			raise CommandError("[%s] alread existed" % new_name)
		obj.name = new_name
		obj.save()
		
		
	def rm(self, *args, **kwargs):
		if len(args) != 1:
			raise UsageError("rm <name>")
		node = Node.current()
			
		name = args[0]
		try:
			obj = Model.objects.get(node=node, name=name)
		except Model.DoesNotExist:
			raise CommandError("[%s] does not exists" % name)
		obj.delete()

