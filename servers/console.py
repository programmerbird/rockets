#-*- coding:utf-8 -*-
import re 
from fabric.api import *
from models import *

env.hosts = ('127.0.0.1',)

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
	
def raise_form_error(form):
	for field in form:
		for error in field.errors:
			raise Exception(field.label + ": " + strip_html(unicode(error)))
	if isinstance(form.non_field_errors, basestring):
		raise Exception (strip_html(form.non_field_errors))
	else:
		raise Exception (strip_html(form.non_field_errors[0]))

def field_value(field):
	try:
		from django import forms
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

def edit_field(form, field_name):
	field = form[field_name]
	
	from django import forms
	if isinstance(field.field, forms.ChoiceField):
		while True:
			print ''
			choices = {}
			i = 0
			for k,v in field.field.choices:
				print '%d - ' % i, v,
				if k==form.values[field_name]:
					print "[selected]"
				else:
					print ""
				choices[unicode(i)] = k
				i += 1
			print ''
			choice = prompt(field.label + ':')
			if choice not in choices:
				continue 
			form.values[field_name] = choices[choice]
			break
	else:
		form.values[field_name] = prompt(field.label + ':', default=form.values[field_name])

def get_form_display_value(form, field_name):
	field = form[field_name]
	from django import forms
	if isinstance(field.field, forms.ChoiceField):
		return dict(field.field.choices).get(form.values[field_name])
	else:
		return form.values[field_name]


def menu(items, ask='Enter a number to select or press ENTER to continue:', null=True):
	while True:
		print '' 
		choices = {}
		i = 0
		for k,label in items:
			choices[unicode(i)] = k
			print '%d - ' % i, label
			i += 1
		print ''
		choice = prompt(ask)
		if null and choice == '':
			return None
		if choice in choices:
			return choices[choice]

def _clean_form(form):
	# clean form
	form.values = getattr(form, 'values', {})
	for x in form.fields:
		form.values[x] = form.values.get(x, field_value(form[x]))

def new_form(form):
	_clean_form(form)
	for x in form.fields:
		if form[x].field.required:
			edit_field(form, x)
	return edit_form(form)
	
def edit_form(form):
	_clean_form(form)
	while True:
		field_name = menu(
			[ (x, form[x].label + ': [ ' + unicode(get_form_display_value(form, x)) + ' ]') for x in form.fields ],
		)
		if field_name is None:
			try:
				if hasattr(form, 'instance'):
					testform = form.__class__(instance=form.instance, data=form.values)
				else:
					testform = form.__class__(data=form.values)
				if testform.is_valid():
					return testform
				raise_form_error(testform)
			except Exception, e:
				print ""
				print "**************************************************************************"
				print unicode(e)
				print "**************************************************************************"
		else:
			edit_field(form, field_name)

