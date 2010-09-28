#!/usr/bin/env python
#-*- coding:utf-8 -*-


from django.conf import settings 

INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])

def load_module(definition):
	module = __import__(definition)	
	components = definition.split('.')
	for component in components[1:]:
		module = getattr(module, component)
	return module
	
def import_class(definition):
	if isinstance(definition, basestring):
		components = definition.split('.')
		module = load_module('.'.join(components[:-1]))
		return getattr(module, components[-1])
	return definition
	
def get_service_name(cls):
	try:
		return cls.Meta.name 
	except:
		n = cls.__name__
		n = n.lower()
		if n.endswith('service'):
			n = n[:(len(n)-len('service'))]
		return n


class ServiceNotFoundException(Exception):
	pass 
	
class PathAppLoader: 
	def get(self, app_name):
		try:
			return self._cache_dict[app_name]
		except KeyError:
			raise ServiceNotFoundException 
			
		except AttributeError:
			self.list()
			return self.get(app_name)
			
	def list(self,):
		try:
			return self._cache_dict.keys()
		except:
			result = {}
			for path in INSTALLED_APPS:
				try:
					app = load_module(path + ".services")
				except ImportError:
					continue
				for attr in dir(app):
					module = getattr(app, attr)
					if hasattr(module, 'get_name'):
						try:
							if module.Meta.abstract:
								continue
						except AttributeError:
							pass
						module._name = name = get_service_name(module)
						if not name:
							continue
						result[name] = module
			self._cache_dict = result 
			return result.keys()
			
			
loader = PathAppLoader()
def list_service_names():
	return loader.list()
	
def list_services():
	return [ x for x in loader.list() ]
	
def get_service(name):
	return loader.get(name)
