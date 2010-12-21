#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, hashlib
from rockets.core import services 
from django import forms

class PublicKeyService(services.Service):
	user = forms.CharField()
	key = forms.CharField()
	
	def template(self):
		return 'publickey'
		
	def preset(self):
		if self.values.get('user')=='root':
			return 'root'
		else:
			return 'user'

	def checksum(self):
		return hashlib.sha1(self.key).hexdigest()
