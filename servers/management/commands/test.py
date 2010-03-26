#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand
from django.db.models.query_utils import CollectedObjects
from django import forms
from servers.console import edit_form
from servers.models import *

class Command(NoArgsCommand):
	help = "Fill wordindex model from tipitaka.models.Paragraph."

	def handle_noargs(self, **options):
		try:

			class NewTestForm (forms.ModelForm):
				class Meta:
					model = Account
			f = NewTestForm()
			edit_form(f)		
		except:	
			import traceback
			traceback.print_exc()

