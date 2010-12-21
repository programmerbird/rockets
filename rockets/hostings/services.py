#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from rockets.core import services 
from django import forms


class MediaService(services.Service):
	name = forms.CharField()
	
	def template(self):
		return 'media'
		
	def preset(self):
		return self.node.os

class UwsgiService(services.Service):
	name = forms.CharField()
	processes = forms.IntegerField(initial=4)
	django_settings = forms.CharField(initial='settings_production')
	
	def add(self, *args, **kwargs):
		self.values['secret'] = os.urandom(5).encode('hex')
		super(UwsgiService, self).add(*args, **kwargs)
		
	def template(self):
		return 'uwsgi'
	
	def plugins(self):
		return [
			('gitdeploy', 'uwsgi-gitdeploy'),
		]
				
	def preset(self):
		return self.node.os
				
	
class PhpService(services.Service):
	name = forms.CharField()
		
	def template(self):
		return 'php'
		
	def preset(self):
		return self.node.os
		
class DomainService(services.Service):
	name = forms.CharField()
	domains = forms.CharField(required=False)
	
	def add(self, name, *args):
		domains = self.values.get('domains', []) or []
		for arg in args:
			if arg not in domains:
				domains.append(arg)
		self.values['domains'] = domains
		self.node.save_service(self)
		self.save()
		self.console.write('%s saved.\n' % self.get_name())
	
	def edit(self, name, *args):
		return self.add(self, name, *args)
	
	def remove(self, name, *args):
		domains = self.values.get('domains', []) or []
		for arg in args:
			if arg in domains:
				domains.remove(arg)
		self.values['domains'] = domains
		self.node.save_service(self)
		self.save()
		self.console.write('%s saved.\n' % self.get_name())

