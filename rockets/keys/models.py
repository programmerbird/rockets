#-*- coding:utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models

class PublicKey(models.Model):
	name = models.CharField(verbose_name=_("name"), max_length=200)
	content = models.TextField()

	def save(self, *args, **kwargs):
		self.content = self.content.strip()
		super(PublicKey, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name 
	
