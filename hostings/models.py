#-*- coding:utf-8 -*-

from django.db import models
from django.db.models import signals
from django.conf import settings
from servers.models import Node 

class Host (models.Model):
	node = models.ForeignKey(Node)	
	
	user = models.CharField(max_length=200)
	application = models.CharField(max_length=200)
	django_settings = models.CharField(max_length=200, default="settings_boatyard")
	
	
class Alias (models.Model):
	host = models.ForeignKey(Host)
	name = models.CharField(max_length=200)

