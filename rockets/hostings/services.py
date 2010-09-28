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
	
	def init(self, *args, **kwargs):
		super(UwsgiService, self).init(*args, **kwargs)
		self.values['secret'] = os.urandom(5).encode('hex')
		
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
		kind = self.get_name()
		self.node.set_service_storage(kind, name, self.values)
		self.save()
		self.console.write('%s saved.\n' % kind.title())
	
	def edit(self, name, *args):
		return self.add(self, name, *args)
	
	def remove(self, name, *args):
		domains = self.values.get('domains', []) or []
		for arg in args:
			if arg in domains:
				domains.remove(arg)
		kind = self.get_name()
		self.node.set_service_storage(kind, name, self.values)
		self.save()
		self.console.write('%s saved.\n' % kind.title())
		
