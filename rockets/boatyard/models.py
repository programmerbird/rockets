#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.db import models

class PublicKey (models.Model):
	
	name = models.CharField(verbose_name=_("PublicKey name"), max_length=200)
	key = models.TextField(required=True)
	


