#-*- coding:utf-8 -*-

import os
from django import forms
from django.conf import settings
from django.utils import simplejson
from django.core.management.base import NoArgsCommand, BaseCommand, CommandError

from rockets.servers.console import menu, new_form, edit_form
from rockets.servers.models import Node
from rockets.servers.template import install_template, uninstall_template
from rockets.servers.api import *
from rockets.hostings.models import Application, APPLICATIONS, APPLICATION_MAP


Model = Application
kind = 'python'
SERVER_DUMP_PATH = getattr(settings, 'SERVER_DUMP_PATH')

class UsageError(CommandError):
	def __init__(self, txt):
		super(UsageError, self).__init__("Usage: rockets pythonweb " + txt)
		
def install(*args):
	manage('install boatyard')
	manage('aptitude install boatyard-nginx-python')

def main(*args):
	node = Node.current()
	if not args:
		for x in Model.objects.filter(node=node).order_by('name'):
			print unicode(x)
		return 
	
	print node
	name = args[0] 
	obj = Model.objects.get(name=name, node=node, kind=kind)
	data=simplejson.loads(obj.options)
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
	obj.options = simplejson.dumps(form.data)
	obj.save()
	
	manage('application dump %s' % name)
	
def add(*args):
	if len(args)!=1:
		raise UsageError("add <name>")
		
	node = Node.current()
	name = args[0]
	if Model.objects.filter(node=node, name=name):
		raise CommandError("[%s] alread existed" % name)
		
	form_class = APPLICATION_MAP[kind]
	class UserForm(form_class):
		user = forms.CharField()
	form = new_form(UserForm())
	p = Model()
	p.name = name 
	p.node = node
	p.kind = form.Meta.name
	p.user = form.data['user']
	del form.data['user']
	p.options = simplejson.dumps(form.data)
	p.save()

	manage('application dump %s' % name)
	
	
def rm(*args):
	if len(args) != 1:
		raise UsageError("rm <name>")
	node = Node.current()
		
	name = args[0]
	try:
		obj = Model.objects.get(node=node, name=name)
	except Model.DoesNotExist:
		raise CommandError("[%s] does not exists" % name)
	data = dict(obj.__dict__)
	data.update({
		'application': obj, 
		'options': obj.params,
	})
	try:
		uninstall_template(node, 
			template = 'hostings/%s' % obj.kind, 
			context=data)
	except TemplateDoesNotExist:
		pass
	obj.delete()

