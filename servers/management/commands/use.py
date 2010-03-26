#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
from django.db.models.query_utils import CollectedObjects
from django import forms
from servers.console import menu, new_form, edit_form
from servers.conf import session 
from servers.models import Node
from fabric.api import *

class UsageError(CommandError):
	def __init__(self, txt):
		super(UsageError, self).__init__("Usage: boatyard use " + txt)

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		if not args:
			try:
				print session.node
				return
			except AttributeError:
				raise CommandError("No node selected")
				
		if len(args) != 1:
			raise UsageError("<servername>")
			
		name = args[0]
		try:
			Node.objects.get(name=name)
			session.node = name
		except Node.DoesNotExist:
			raise CommandError("[%s] does not exists")

