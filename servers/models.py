#-*- coding:utf-8 -*-

from django import forms
from django.db import models
from django.db.models import signals
from django.conf import settings
from django.utils import simplejson as json
from libcloud.types import Provider as types
from libcloud.providers import get_driver
import os 

class RackspaceDriver (forms.Form):
	username = forms.CharField()
	api_key = forms.CharField()
	class Meta:
		slug = 'RACKSPACE'
		fields = ('username', 'api_key',)

class SlicehostDriver (forms.Form):
	api_key = forms.CharField()
	class Meta:
		slug = 'SLICEHOST'
		fields = ('api_key',)


class EC2Driver (forms.Form):
	access_key_id = forms.CharField()
	secret_key = forms.CharField()
	class Meta:
		slug = 'EC2'
		fields = ('access_key_id', 'secret_key',)

STORE_ROOT_PASSWORD = getattr(settings, 'STORE_ROOT_PASSWORD', True)

DRIVERS = [
	EC2Driver,
	SlicehostDriver,
	RackspaceDriver,
]

DRIVERS_MAP = dict([ (getattr(types, x.Meta.slug), x) for x in DRIVERS ])
DRIVERS_CHOICES = [ (getattr(types, x.Meta.slug), x.Meta.slug) for x in DRIVERS ]

class Provider (models.Model):
	name = models.CharField(max_length=200)
	driver = models.IntegerField(choices=DRIVERS_CHOICES)
	storage = models.TextField()
	
	def get_storage(self):
		try:
			return self._storage
		except AttributeError:
			self._storage = s = json.loads(self.storage)
			return s 
			
	def get_driver(self):
		try:
			return self._driver 
		except AttributeError:
			fields = DRIVERS_MAP[self.driver].Meta.fields
			storage = self.get_storage()
			args = [ storage[x] for x in fields ]
			self._driver = d = get_driver(self.driver)(*args)
			return d 
			
	def get_driver_name(self):
		return DRIVERS_MAP[self.driver].Meta.slug
			
	def __unicode__(self):
		return self.name
		
	def get_node(self, name):
		if isinstance(name, Node):
			name = node.name
		if isinstance(name, basestring):
			nodes = self.get_driver().list_nodes()
			for x in nodes:
				if x.name == name:
					return x
		return name

	def set_password(self, node, password):
		driver_name = self.get_driver_name()
		if driver_name == 'RACKSPACE':
			node = self.get_node(node)
			if not node:
				raise Exception("[%s] unknown node" % node)
			uri = "/servers/%s" % node.id
			body = json.dumps({
				"server": {
					"name": node.name, 
					"adminPass": password,
				}
			})
			resp = self.get_driver().connection.request(uri, method='PUT', data=body)
			return resp 
		raise NotImplemented
		
class Session(models.Model):
	name = models.CharField(max_length=200, primary_key=True)
	value = models.TextField()


class NoNodeSelected(Exception):
	pass 

class Node(models.Model):
	name = models.CharField(max_length=200)
	provider = models.ForeignKey(Provider, null=True, editable=False)
	services = models.TextField(null=True, blank=True, editable=False)
	storage = models.TextField(null=True, blank=True, editable=False)
	
	username = models.CharField(max_length=200, default='root')
	password = models.CharField(max_length=200, null=True, blank=True, editable=False)
	
	public_ip = models.TextField(null=True, blank=True)
	private_ip = models.TextField(null=True, blank=True)
	
	@classmethod
	def current(cls):
		try:
			name = Session.objects.get(name='node').value
			return Node.by_name(name)
		except Session.DoesNotExist:
			raise NoNodeSelected()
			
	def set_password(self, password):
		if self.provider:
			return self.provider.set_password(self.name, password)
		raise NotImplemented
			
	def get_password(self):
		if self.password:
			return self.password 
		password = os.urandom(8).encode('hex')
		self.set_password(password)
		if STORE_ROOT_PASSWORD:
			self.password = password 
			self.save()
		return password 
			
	def get_services(self):
		try:
			return self._services
		except AttributeError:
			self._services = s = json.loads(self.services or '[]')
			return s 
			
	def get_storage(self):
		try:
			return self._storage
		except AttributeError:
			self._storage = s = json.loads(self.storage or '{}')
			return s 
				
	def get_service_storage(self, service):
		return self.get_storage().get(service, {})
		
	def set_service_storage(self, service, value):
		self.get_storage()[service] = value 
		
	def get_private_ip(self):
		try:
			return self._private_ip
		except AttributeError:
			if not self.private_ip:
				self._private_ip = s = self.get_connection().private_ip
				self.private_ip = json.dumps(s)
				self.save()
				return s
			self._private_ip = s = json.loads(self.private_ip)			
			return s

	def get_public_ip(self):
		try:
			return self._public_ip
		except AttributeError:
			if not self.public_ip:
				self._public_ip = s = self.get_connection().public_ip
				self.public_ip = json.dumps(s)
				self.save()
				return s
			self._public_ip = s = json.loads(self.public_ip)			
			return s
					
	def get_connection(self):
		try:
			return self._conn
		except:
			if self.provider:
				driver = self.provider.get_driver()
				for x in driver.list_nodes():
					if x.name == self.name:
						self._conn = x 
						return x 
			self._conn = None
		
	@classmethod 
	def get(self, provider, name):
		return Node.objects.get_or_create(provider=provider, name=name)
		
	@classmethod 
	def by_name(self, name):
		try:
			return Node.objects.get(name=name)
		except Node.DoesNotExist:
			providers = Provider.objects.all()
			for provider in providers:
				nodes = provider.get_driver().list_nodes()
				for node in nodes:
					if node.name == name:
						return Node.get(provider, name)
			raise Node.DoesNotExist
			
	def save(self, *args, **kwargs):
		if hasattr(self, '_storage'):
			self.storage = json.dumps(self._storage)
		if hasattr(self, '_services'):
			self.services = json.dumps(self._services)
		if self.public_ip and not self.public_ip.startswith('['):
			self.public_ip = json.dumps([self.public_ip])
		if self.private_ip and not self.private_ip.startswith('['):
			self.private_ip = json.dumps([self.private_ip])
		super(Node, self).save(*args, **kwargs)
			
	def __unicode__(self):
		return self.name
		

		
