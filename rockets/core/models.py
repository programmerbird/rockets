#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
import uuid
from django.db import models
from django.db.models import Q, signals
from django.conf import settings

class Session(models.Model):
	name = models.CharField(max_length=200, primary_key=True)
	value = models.TextField()

	@classmethod
	def get(self, name, default=None):
		try:
			session = Session.objects.get(name=name)
			return session.value
		except Session.DoesNotExist:
			if default:
				self.store(name, default)
			return default 
			
	@classmethod 
	def store(self, name, value):
		session, is_created = Session.objects.get_or_create(name=name)
		session.value = value
		session.save()
		
	@classmethod
	def bundle(self,):
		return self.get("rocket_bundle", default=unicode(uuid.uuid4()))
		
class NoNodeSelected(Exception):
	def __unicode__(self):
		return "No node selected"

class Listener(models.Model):
	node = models.CharField(max_length=200, default='*')
	service = models.CharField(max_length=200, default='*')
	service_name = models.CharField(max_length=200, default='*')
	action = models.CharField(max_length=200, default='*')
	
	name = models.CharField(max_length=200, primary_key=True)
	method = models.CharField(max_length=200)
	parameters = models.TextField(null=True, blank=True)
	
	@classmethod 
	def dispatch(self, node, service, name, action):	
		listeners = Listener.objects.filter(Q(node=node)|Q(node='*')) \
			.filter(Q(service=service)|Q(service='*')) \
			.filter(Q(service_name=name)|Q(name='*')) \
			.filter(Q(action=action)|Q(action='*'))
		for listener in listeners:
			listener.sender = node 
			listener.sender_service = service 
			listener.sender_service_name = service_name 
			listener.sender_action = action
			listener.invoke()
	
	def invoke(self):
		pass 
		
class ServiceDoesNotExist(Exception):
	pass
		
class Node (models.Model):
	name = models.CharField(max_length=200, unique=True)
	public_ip = models.TextField(null=True, blank=True)
	private_ip = models.TextField(null=True, blank=True)
	
	provider = models.CharField(max_length=200, null=True, blank=True)
	os = models.CharField(max_length=200, null=True, blank=True, default='ubuntu')
	username = models.CharField(max_length=200, blank=True, default='root')
	port = models.IntegerField(default=22)
	
	services = models.TextField(blank=True, default='[]')
	storage = models.TextField(blank=True, default='{}')
	
	@classmethod
	def current(self):
		name = Session.get('node')
		if not name:
			name = "localhost"
		return Node.objects.get(name=name)
		
	def get_storage(self):
		try:
			return self._storage 
		except AttributeError:
			self._storage = s = json.loads(self.storage or '{}')
			return s 
			
	def get_services(self):
		try:
			return self._services
		except AttributeError:
			self._services = s = json.loads(self.services or '[]')
			return s 
			
	def installed(self, kind, name=None):
		storage = self.get_storage()
		for pk, service_storage in storage.items():
			service_kind = service_storage.get('kind')
			service_name = service_storage.get('name')
			if kind != service_kind:
				continue
			if not name:
				return True
			if name != service_name:
				continue
			return True
		return False
		
	def service(self, pk):
		import loaders
		(kind, name) = pk.split(':', 1)
		data = self.get_storage().get(pk, {})
		if data is None:
			raise ServiceDoesNotExist
		else:
			n = loaders.get_service(kind)()
			n.pk = pk
			n.node = self
			n.kind = kind
			n.name = name
			n.deserialize(data.get('storage') or {})
			n.values['name'] = name
			return n
		
	def get_or_create_service(self, pk):
		import loaders
		(kind, name) = pk.split(':', 1)
		n = loaders.get_service(kind)()
		data = self.get_storage().get(pk, {})
		is_created = data is None
		n.pk = pk
		n.node = self
		n.kind = kind
		n.name = name
		n.deserialize(data.get('storage') or {})
		n.values['name'] = name
		return n, is_created
		
	def save_service(self, service):
		storage = self.get_storage()
		kind = service.kind 
		name = service.name
		pk = '%s:%s' % (kind, name)
		storage[pk] = {
			'name': service.name,
			'kind': service.kind,
			'storage': service.serialize(),
		}

	def _manage_json_fields(self):
		if hasattr(self, '_storage'):
			self._fix_services_names()
			self.storage = json.dumps(self._storage)
		if hasattr(self, '_services'):
			self.services = json.dumps(self._services)
	
	def _fix_services_names(self):
		storage = self.get_storage()
		new_storage = {}
		for service, datastore in storage.items():
			result = {}
			name = datastore.get('name')
			kind = datastore.get('kind')
			pk = '%s:%s' % (kind, name)
			new_storage[pk] = datastore			 
		self.storage = new_storage 
		self._services = self.storage.keys()
		
	def _manage_ip_fields(self):
		if self.public_ip and not self.public_ip.startswith('['):
			self.public_ip = json.dumps([self.public_ip])
		if self.private_ip and not self.private_ip.startswith('['):
			self.private_ip = json.dumps([self.private_ip])
	
	def save(self, *args, **kwargs):
		self._manage_json_fields()
		self._manage_ip_fields()
		super(Node, self).save(*args, **kwargs)
		
	def resolve_plugins(self, name=None, excludes=[]):
		storage = self.get_storage()
		for pk, service_storage in storage.items():
			service_name = service_storage.get('name')
			if pk in excludes:
				continue
			if name and service_name != name:
				continue
			service = self.service(pk) 
			service.install_plugins(force=False)				

	def __unicode__(self):
		return self.name

