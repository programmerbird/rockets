#!/usr/bin/env python
#-*- coding:utf-8 -*-

from rockets import services 
from django import forms


class MediaService(services.Service):
	name = forms.CharField()
	
	def template(self):
		return 'media'
		
	def preset(self):
		return self.node.os

class UwsgiService(services.Service):
	name = forms.CharField()
	
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
		
