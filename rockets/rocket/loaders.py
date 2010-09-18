#!/usr/bin/env python
#-*- coding:utf-8 -*-


from django.conf import settings 
from hibird.utils import import_class, load_module

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
			for path in ROCKETS_APPS:
				app = import_class(path)
				for attr in dir(app):
					module = getattr(app, attr)
					if hasattr(module, 'get_name'):
						name = module.get_name()
						result[name] = module
			self._cache_dict = result 
			return result.keys()
			
			
loader = PathAppLoader()
def list_service_names():
	return loader.list()
	
def list_services():
	return [ loader.get(x) for x in loader.list() ]
	
def get_service(name):
	return loader.get(name)
