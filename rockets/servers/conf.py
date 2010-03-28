#-*- coding:utf-8 -*-


from models import Session 

class SessionObject(object):	
	def __getattr__(self, name):
		try:
			session = Session.objects.get(name=name)
			return session.value
		except Session.DoesNotExist:
			raise AttributeError
	
	def __setattr__(self, name, value):
		session, is_created = Session.objects.get_or_create(name=name)
		session.value = value
		session.save()
		
session = SessionObject()

