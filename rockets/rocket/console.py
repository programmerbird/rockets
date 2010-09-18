#-*- coding:utf-8 -*-
import re 
import time
from django import forms
from models import *

from django.core.management.base import CommandError

HTML_RULES = (
	(re.compile('\<br\W*\>'), '\n'),
	(re.compile('\<\/?(div|p|table|tr)>'), '\n'),
	(re.compile('\&nbsp\;'), ' '),
	(re.compile('\<.*?\>'), ''),
)

	
def strip_html(value):
	value = unicode(value or '')
	for pattern, replace in HTML_RULES:
		value = pattern.sub(replace, value)
	return value
	
def field_value(field):
	try:
		value = field.form.data.get(field.name)
		if value:
			return value
		value = field.form.initial.get(field.name)
		if value:
			return value
		if isinstance(field.field, forms.ChoiceField):
			value = unicode(value)
			for (val, desc) in field.field.choices:
		 		if val == value:
		 			return desc
		return value or ""
	except:
		pass
		
		
def get_form_display_value(form, field_name):
	field = form[field_name]
	if isinstance(field.field, forms.ChoiceField):
		return dict(field.field.choices).get(form.values[field_name])
	else:
		return form.values[field_name]

			
class Console(object):

	command = None

	def write(self, text):
		if self.command:
			self.command.stdout.write(text)
		else:
			print text 
		
	def raise_exception(self, exception):
		if self.command:
			raise CommandError(unicode(exception))
		else:
			raise exception
			
	def write_exception(self, exception):
		if self.command:
			self.command.stderr.write("\033[22;31mError: %s\033[0;0m\n" % unicode(exception))
			time.sleep(0.2)
		else:
			print unicode(exception)
			
			
	def read(self, text=None):
		return raw_input("\033[01;32m%s\033[0;0m" % text)
		
	def prompt(self, text='', default=None, null=True, choices=None):
		text += '\033[0;0m :'
		if default:
			text += ' [%s]' % unicode(default).strip()
		value = None 
		while value is None:
			value = self.read('%s ' % text) or default 
			if null and value is None:
				break
			if choices:
				if value not in choices:
					continue
		return value

	def menu(self, items, ask=None, null=True, default=None):
		if not ask:
			if null:
				ask = 'Select a number [or ENTER to exit]'
			else:
				ask = 'Select a number'		
		if not items:
			return None
		if len(items)==1 and not null:
			return items[0][0]
		while True:
			choices = {}
			i = 0
			for k,label in items:
				choices[unicode(i)] = k
				if k == default:
					default_text = '[selected]'
				else:
					default_text = ''
				self.write('  %2d - %s %s\n' % (i, label, default_text))
				i += 1
			choice = self.prompt(ask, null=null)
			if null and choice is None:
				return default
			if choice is not None and choice in choices:
				return choices[choice]

	def edit_field(self, form, field_name):
		field = form[field_name]
		value = form.values[field_name]
		if isinstance(field.field, forms.ChoiceField):
			value = self.menu(field.field.choices, null=True, default=value)
		else:
			value = self.prompt("       %s" % field.label, default=value)
		form.values[field_name] = value
		

	def _clean_form(self, form):
		# clean form
		form.values = getattr(form, 'values', {})
		for field in form.fields:
			form.values[field] = form.values.get(field, field_value(form[field]))

	def is_form_valid(self, form):
		if hasattr(form, 'instance'):
			testform = form.__class__(instance=form.instance, data=form.values)
		else:
			testform = form.__class__(data=form.values)
		if testform.is_valid():
			return True
		self.raise_form_error(testform)
		

	def raise_form_error(self, form):
		msg = None
		for field in form:
			for error in field.errors:
				msg = strip_html(unicode(error))
				if "This field" in msg:
					msg = msg.replace("This field", field.label)
				else:
					msg = field.label + ": " + msg
				break
			if msg:
				break
		if not msg and isinstance(form.non_field_errors, basestring):
			msg = strip_html(form.non_field_errors)
		if not msg:
			msg = strip_html(form.non_field_errors[0])
		if not msg:
			msg = "There's something wrong with this form"
		self.raise_exception(msg)
		
		
	def new_form(self, form):
		self._clean_form(form)
		for field in form.fields:
			if form[field].field.initial:
				form.values[field] = form[field].field.initial
		
		while True:
			self.write("Enter the new value, or press ENTER for the default\n")
			for field in form.fields:
				self.edit_field(form, field)
			try:
				if self.is_form_valid(form):
					self.write('\n')
					return 
			except Exception, e:
				self.write_exception(e)

	def edit_form(self, form):
		self._clean_form(form)
		while True:
			self.write("Select the following choices to edit the value\n")
			field_name = self.menu(
				[ (x, '%-15s: %s' % (form[x].label, unicode(get_form_display_value(form, x)).strip() or '--')) for x in form.fields ],
			)
			if field_name:
				self.edit_field(form, field_name)
			else:
				try:
					if self.is_form_valid(form):
						self.write('\n')
						return 
				except Exception, e:
					self.write_exception(e)
				
		
