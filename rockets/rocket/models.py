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
			
	def get_services(self, service):
		try:
			return self._services
		except AttributeError:
			self._services = s = json.loads(self.services or '[]')
			return s 
			
	def installed(self, service, name=None):
		storage = self.get_storage()
		s = storage.get(service)
		if not s:
			return False 
		if not name:
			return True 
		return name in s 			
		
	def get_services_storage(self, service):
		storage = self.get_storage()
		if service not in storage:
			services_storage = storage[service] = {}
		else:
			services_storage = storage[service] 
		return services_storage
			
	def get_service_storage(self, service, name):
		services_storage = self.get_services_storage(service)
		if name not in services_storage:
			service_storage = services_storage[name] = {}
		else:
			service_storage = services_storage[name]
		return service_storage 
		
			
	def set_service_storage(self, service, name, values):
		services_storage = self.get_services_storage(service)
		if name not in services_storage:
			service_storage = services_storage[name] = {}
		else:
			service_storage = services_storage[name]
		services_storage[name] = values
		

	def _manage_json_fields(self):
		if hasattr(self, '_storage'):
			self._fix_services_names()
			self.storage = json.dumps(self._storage)
		if hasattr(self, '_services'):
			self.services = json.dumps(self._services)
	
	def _fix_services_names(self):
		storage = self.get_storage()
		new_storage = {}
		for service, children in storage.items():
			result = {}
			for key, data in children.items():
				result[data.get('name')] = data 
			new_storage[service] = result 
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
		

	def __unicode__(self):
		return self.name			
