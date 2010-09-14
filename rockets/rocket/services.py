#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
from utils import hashdict
from models import * 

class Service(forms.Form):
	node = None
	service = None
	service_name = None 
	storage = None 
	template = None
	
	def __init__(self, *args, **kwargs):
		super(Service, self).__init__(*args, **kwargs)
		self.listeners()
		
	def add(self, *args, **kwargs):
		self.storage.update(kwargs)
		self.confirm_save(*args, **kwargs)
		
	def edit(self, *args, **kwargs):
		self.storage.update(kwargs)
		self.confirm_save(*args, **kwargs)
		
	def remove(self, *args, **kwargs):
		self.storage.update(kwargs)
		self.confirm_remove(*args, **kwargs)
		
	def confirm_save(self, *args, **kwargs):
		if not kwargs.get('force'):
			if not self.console():
				return
		self.save()
	
	def confirm_remove(self, *args, **kwargs):
		if not kwargs.get('force'):
			if not self.console():
				return
		self.remove()
		
	def console(self):
		return True 
		
	def dump(self, ):
		pass 
		
	def remove(self):
		self.uninstall_listeners()
		pass 
		
		
	def save(self):
		self.dispatch('pre_save')
		self.uninstall_listeners()
		self.dump()
		self.node.save()
		self.listeners()
		self.install_listeners()
		self.dispatch('post_save')
		
	def dispatch(self, action=None):
		Listener.dispatch(node=self.node.name, service=self.service, service_name=self.service_name, action=action)
		
	def listeners(self):
		pass 
		
	def install_listeners(self):
		for x in self._listeners:
			x.save()
			
	def uninstall_listeners(self):
		for x in self._listeners:
			x.delete()
			
	def listen(self, method, node='*', service='*', service_name='*', action='*'):
		data = {
			"method": "rocket.services.invoke",
			"parameters": json.dumps({
				'class_name': self.__class__.__name__,
				'node_name': self.node.name,
				'service': self.service,
				'service_name': self.service_name,
				'method': method,
			}),
			"node": node,
			"service": service, 
			"service_name": service_name,
			"action": action,
		}
		pk = hashdict(data)
		data['name'] = pk
		listener = Listener(**data)
		self.listeners.append(listener)
		return listener
			
		
def invoke(listener, class_name, node_name=None, service=None, service_name=None, method=None):
	pass 

