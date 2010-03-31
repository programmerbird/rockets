#-*- coding:utf-8 -*-

import os 
from django.db import models
from django.db.models import signals
from django.conf import settings
from rockets.servers.models import Node 
from django import forms
from django.utils import simplejson 
from django.utils.translation import ugettext_lazy as _

class PythonApplication(forms.Form):
	process = forms.IntegerField(initial=6)
	harakiri = forms.IntegerField(initial=6)
	additional = forms.CharField(initial='', required=False)
	
	django_settings = forms.CharField(initial='settings_boatyard')
	class Meta:
		name = 'python' 

class PhpApplication(forms.Form):
	class Meta:
		name = 'php' 

APPLICATIONS = (
	PythonApplication,
	PhpApplication,
)
APPLICATION_KINDS = [ (x.Meta.name, x.Meta.name) for x in APPLICATIONS ]
APPLICATION_MAP = dict([ (x.Meta.name, x) for x in APPLICATIONS ])

class Application (models.Model):
	name = models.CharField(max_length=200)
	node = models.ForeignKey(Node)	
	user = models.CharField(max_length=200)
	secret = models.CharField(max_length=200)
	kind = models.CharField(max_length=10, choices=APPLICATION_KINDS)
	options = models.TextField(null=True, blank=True)
	
	def _manage_secret(self):
		if not self.secret:
			self.secret = os.urandom(8).encode('hex')

	def save(self, *args, **kwargs):
		self._manage_secret()
		super(Application, self).save(*args, **kwargs)
		
	def __unicode__(self):
		return self.name
		
	def params(self):
		try:
			return self._params
		except AttributeError:
			self._params = s = simplejson.loads(self.options or '{}')
			return s

class Alias (models.Model):
	application = models.ForeignKey(Application)
	name = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.name

