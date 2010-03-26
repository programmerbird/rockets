#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
from django.db.models.query_utils import CollectedObjects
from django import forms
from servers.console import menu, new_form, edit_form
from servers.models import Provider, Node

class NodeForm (forms.ModelForm):
	class Meta:
		model = Node

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		node = Node.current()
		form = NodeForm(instance=node)
		form = edit_form(form)
		form.save(commit=True)
		print "saved", node
		

