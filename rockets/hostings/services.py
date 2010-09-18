#!/usr/bin/env python
#-*- coding:utf-8 -*-

from rocket.services import Service 
from django import forms


class Media(Service):
	name = forms.CharField()
	
class Uwsgi(Service):
	name = forms.CharField()
	
class Php(Service):
	name = forms.CharField()
