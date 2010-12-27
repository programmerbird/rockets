#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from rockets.core import services 
from django import forms


class GitDeployService(services.Service):
	name = forms.CharField()
	
	def template(self):
		return 'gitdeploy'
		
	def preset(self):
		return 'all'

