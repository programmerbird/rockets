#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from rockets import services 
from django import forms


class MediaService(services.Service):
	name = forms.CharField()
	
	def template(self):
		return 'media'
		
	def preset(self):
		return self.node.os
		
class DomainService(services.Service):
	
	def install(self):
		pass
		
	def init(self, name, *args, **kwargs):
		self.name = name
		self.values = self.node.get_service_storage(self.get_name(), name)
	
	def get_domains_list(self):
		old = self.node.get_service_storage(self.get_name(), self.name)
		self.values = old
		if not old:
			old = {}
		if 'names' not in old:
			old['names'] = []
		return old['names']
		
	def add(self, *args, **kwargs):
		domain = args[1]
		domains = self.get_domains_list()
		domains.append(domain)
		self.values['names'] = list(set(domains))
		print "Current domains:"
		for x in self.get_domains_list():
			print "-", x
		self.confirm_save(*args, **kwargs)
		
	def edit(self, *args, **kwargs):
		print "Current domains:"
		for x in self.get_domains_list():
			print "-", x
		
	def remove(self, *args, **kwargs):
		domain = args[1]
		domains = self.get_domains_list()
		result = [ x for x in domains if x != domain ]
		self.values['names'] = list(set(result))
		print "Current domains:"
		for x in self.get_domains_list():
			print "-", x
		self.confirm_save(*args, **kwargs)

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
		self.plugin('gitdeploy', 'uwsgi-gitdeploy'),
				
	def preset(self):
		return self.node.os
				
	
class PhpService(services.Service):
	name = forms.CharField()
		
	def template(self):
		return 'php'
		
	def preset(self):
		return self.node.os
		
