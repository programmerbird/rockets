#!/usr/bin/env python
#-*- coding:utf-8 -*-


from django import template
from django.template import Variable
from rockets.rocket.models import Node 

register = template.Library()

class ServiceDataNode(template.Node):
	def __init__(self, service, name, var_name):
		self.service = service
		self.name = name
		self.var_name = var_name
		
	def render(self, context):
		name = Variable(self.name).resolve(context)
		context[self.var_name] = Node.current().get_service_storage(self.service, name)
		return ''

"""
	{% servicedata domain "boatyardapp" as domains %}
"""
def do_service_data(parser, token):
	try:
		# split_contents() knows not to split quoted strings.
		SERVICE_DATA, service, name, AS, var_name = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
	return ServiceDataNode(service, name, var_name)
	
register.tag('servicedata', do_service_data)
