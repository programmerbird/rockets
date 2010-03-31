#-*- coding:utf-8 -*-



from django.db import models
from django.conf import settings
from rockets.servers.models import Node

class Proxy (models.Model):
	node = models.ForeignKey(Node)	
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name
