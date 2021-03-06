#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os 
import json
from django import forms
from utils import hashdict
from models import * 
import console
import templates
import conf


SERVER_DUMP_PATH = getattr(settings, 'SERVER_DUMP_PATH', '/tmp')
class DuplicateServiceNameException(Exception):
	def __unicode__(self):
		return "Duplicate service name already existed"
		
class BaseService(forms.Form):
		
	def __init__(self, *args, **kwargs):
		super(BaseService, self).__init__(*args, **kwargs)
		self.console = console.Console()
		self.name = None
		self.values = {}
		self._listeners = []
		self._plugins = []
		self.listeners()
		
		
	def add(self, *args, **kwargs):
		self.values.update(kwargs)
		self.console.new_form(self)
		self.confirm_save(*args, **kwargs)
		
	# load values into self.values 
	# call after __init__, before edit and remove operations
	def load(self, name, *args, **kwargs):
		self.name = name
		self.values = self.node.get_service_storage(self.get_name(), name)
		self.values['name'] = name
		
	# load values into self.values 
	# call after __init__, before add operations
	def init(self, name, *args, **kwargs):
		self.name = name
		self.values = self.node.get_service_storage(self.get_name(), name)
		if self.values:
			raise DuplicateServiceNameException
			
		self.values['name'] = name
		
	def edit(self, *args, **kwargs):
		self.values.update(kwargs)
		
		self.console.edit_form(self)
		self.confirm_save(*args, **kwargs)
		
	def remove(self, *args, **kwargs):
		self.confirm_delete(*args, **kwargs)
		
		
	@classmethod
	def get_name(self):
		try:
			return self._name 
		except AttributeError:
			try:
				self._name = n = self.Meta.name 
			except:
				n = self._module_name
				n = n.lower()
				if n.endswith('service'):
					n = n[:(len(n)-len('service'))]
				self._name = n 
			return n
			 
	def require(self, package):
		self.node.install(package)

	def confirm_save(self, *args, **kwargs):
		kind = self.get_name()
		name = self.values.get('name', '')
		if conf.SAVE_CONFIRMATION and not kwargs.get('force'):
			while True:
				result = self.console.prompt("Is the information correct? \033[0;0m[Y/n]", null=False, choices="Yyn")
				if result in 'Yy':
					break
				self.console.edit_form(self)
		self.node.set_service_storage(kind, name, self.values)
		self.save()
		self.console.write('%s saved.\n' % kind.title())
	
	def confirm_delete(self, *args, **kwargs):
		kind = self.get_name()
		name = self.values.get('name', '')
		if conf.DELETE_CONFIRMATION and not kwargs.get('force'):
			self.console.write('You are going to remove the following item(s):\n')
			self.console.write('  - %s (%s)\n' % (name, kind))
			result = self.console.prompt("Are you sure you want to do this? \033[0;0m[Y/n]", null=False, choices="Yyn")
			if result in 'n':
				return
		self.delete()
		self.console.write('%s removed.\n' % kind.title())
		
	def dumps(self, template, script=None, preset=None, context=None):
		if not script:
			script = 'install'
		if not preset:
			preset = self.preset()
		if not context:
			context = {}
		
		template_context = {"node": self.node, "rocket_bundle": Session.bundle()}
		template_context.update(self.values)
		template_context.update(context)
		
		source_path = os.path.join(template, preset)
		target_path = ''
		
		if script == 'install':
			templates.install_template(self.node, source_path, context=template_context)
		elif script == 'uninstall':
			templates.uninstall_template(self.node, source_path, context=template_context)
		
		
	def dispatch(self, action=None):
		Listener.dispatch(node=self.node.name, 
			service=self.get_name(), 
			name=self.name, 
			action=action)
		
	def install_listeners(self):
		for x in self._listeners:
			x.save()
			
	def uninstall_listeners(self):
		for x in self._listeners:
			x.delete()
			
	def plugin(self, package, template):
		self._plugins += (package, template),
			
		
	def install(self):
		tmp = self.template()
		if isinstance(tmp, basestring):
			context = None 
			template = tmp
		else:
			(template, context) = tmp 
		self.deploy(template, context=context)
		self._plugins = []
		self.plugins()
		print self._plugins
		for (package, plugin_template) in self._plugins:
			print 'check', package, self.name
			if self.node.installed(package, self.name):
				self.deploy(plugin_template, context=context)
	
	def uninstall(self):
		tmp = self.template()
		if isinstance(tmp, basestring):
			context = None 
			template = tmp
		else:
			(template, context) = tmp 
		self.undeploy(template, context=context)
		self._plugins = []
		self.plugins()
		for (package, plugin_template) in self._plugins:
			if self.node.installed(package, self.name):
				self.undeploy(plugin_template, context=context)
	

	def listen(self, method, node='*', service='*', name='*', action='*'):
		data = {
			"method": "rocket.services.invoke",
			"parameters": json.dumps({
				'class_name': self.__class__.__name__,
				'node_name': self.node.name,
				'service': self.get_name(),
				'name': self.name,
				'method': method,
			}),
			"node": node,
			"service": service, 
			"name": name,
			"action": action,
		}
		pk = hashdict(data)
		data['name'] = pk
		listener = Listener(**data)
		self.listeners.append(listener)
		return listener
		
		

	def delete(self):
		self.dispatch('pre_remove')
		self.uninstall_listeners()
		self.uninstall()
		self.dispatch('post_remove')
				
	def save(self):
		self.dispatch('pre_save')
		self.uninstall_listeners()
		self.node.save()
		self.install()
		self.listeners()
		self.install_listeners()
		self.dispatch('post_save')
				
	def deploy(self, template=None, context=None, preset=None):
		self.dumps(template, script='install', preset=preset, context=context)
		
	def undeploy(self, template=None, context=None, preset=None):
		self.dumps(template, script='uninstall', preset=preset, context=context)
		
			
	class Meta:
		abstract = True
		
class Service(BaseService):
	node = None
	name = None 
	
	def listeners(self):
		pass 
	
	def requirements(self):
		pass
		
	def template(self):
		return 
		
	def preset(self):
		return "generic"
		
	def plugins(self):
		pass
		
	def template(self):
		pass 
		
	class Meta:
		pass
		
def invoke(listener, class_name, node_name=None, service=None, name=None, method=None):
	pass 
	
class NodeService(Service):
	# node = some models.Node instance 
	# name = None 
	
	name = forms.CharField()
	public_ip = forms.CharField(required=False)
	private_ip = forms.CharField(required=False)
	
	provider = forms.CharField(required=False,)
	os = forms.CharField(required=False, initial='ubuntu')
	username = forms.CharField(required=False, initial='root')
	
	def init(self, name=None):
		if name:
			self.name = name 
			self.values['name'] = name
		self.node = Node()
	
	def load(self, name, *args, **kwargs):
		self.node = node = Node.objects.get(name=name)
		self.values = {}
		for field in self:
			self.values[field.name] = getattr(node, field.name)
			
	def install(self):					
		for field in self:
			setattr(self.node, field.name, self.values[field.name])
		self.node.save()

	def uninstall(self):
		self.node.delete()
	

