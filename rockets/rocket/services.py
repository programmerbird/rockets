#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
from utils import hashdict
from models import * 

class BaseService(forms.Form):
		
			
	def __init__(self, *args, **kwargs):
		super(Service, self).__init__(*args, **kwargs)
		self.service_name = None
		self.listeners()
		
	def get_name(self):
		try:
			return self._name 
		except AttributeError:
			try:
				self._name = n = self.Meta.name 
			except:
				n = self.__class__.__name__
				n = full_name.lower()
				if n.endswith('service'):
					n = n[:(len(n)-len('service'))]
				self._name = n 
			return n
			 
	def require(self, package):
		self.node.install(package)

	def confirm_save(self, *args, **kwargs):
		if not kwargs.get('force'):
			if not self.console():
				return
		self.save()
	
	def confirm_delete(self, *args, **kwargs):
		if not kwargs.get('force'):
			if not self.console():
				return
		self.delete()
		
	def console(self):
		return True 
		
	def dump(self, script=None):
		if not script:
			script = 'install'
		
	def dispatch(self, action=None):
		Listener.dispatch(node=self.node.name, 
			service=self.get_name(), 
			service_name=self.service_name, 
			action=action)
		
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
				'service': self.get_name(),
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
			
		
class Service(BaseService):
	node = None
	service_name = None 
	
	def listeners(self):
		pass 
	
	def requirements(self):
		pass
		
	def add(self, *args, **kwargs):
		self.confirm_save(*args, **kwargs)
		
	# load values into self.values 
	# call after __init__, before edit and remove operations
	def load(self, *args, **kwargs):
		pass 
		
	def edit(self, *args, **kwargs):
		self.storage.update(kwargs)
		self.confirm_save(*args, **kwargs)
		
	def remove(self, *args, **kwargs):
		self.confirm_delete(*args, **kwargs)
		

	def delete(self):
		self.dispatch('pre_remove')
		self.uninstall_listeners()
		self.uninstall()
		self.dispatch('post_remove')
				
	def save(self):
		self.dispatch('pre_save')
		self.uninstall_listeners()
		self.install()
		self.node.save()
		self.listeners()
		self.install_listeners()
		self.dispatch('post_save')
		
	def install(self):
		pass 
		
	def uninstall(self):
		pass 
		
def invoke(listener, class_name, node_name=None, service=None, service_name=None, method=None):
	pass 
	
class NodeService(Service):
	# node = some models.Node instance 
	# service_name = None 
	
	name = forms.CharField()
	public_ip = forms.CharField(required=False)
	private_ip = forms.CharField(required=False)
	
	provider = forms.CharField(required=False,)
	os = forms.CharField(required=False, initial='ubuntu')
	username = forms.CharField(required=False, initial='root')
	
	def add(self, *args, **kwargs):
		self.node = node = Node(**self.values)
	
	def load(self, name, *args, **kwargs):
		self.node = node = Node.objects.get(name=name)
		self.values = {}
		for field in self:
			self.values[field] = getattr(node, field)
	
