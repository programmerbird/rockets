#-*- coding:utf-8 -*-
"""
Install SSH Public Key

usage: 

rockets node [nodename] authorized_keys add [keyname] to [username] 
rockets node [nodename] authorized_keys add [keyname] // username==keyname

"""
from rockets.servers.api import *
from rockets.servers.template import install_template, uninstall_template
from rockets.hostings.models import Application, Alias
from rockets.reverseproxies.models import Proxy

def install(*args):
	manage('install boatyard')
	manage('aptitude install boatyard boatyard-nginx')
	
def main(*args):
	node = env.node 
	proxies = Proxy.objects.filter(node=node).order_by('name')
	for proxy in proxies:
		applications = Application.objects.filter(name=proxy.name)
		if not applications:
			continue
		nodes = Node.objects.filter(application__in=applications)
		domains = Alias.objects.filter(application__in=applications)
		application = applications[0]
		
		data = dict(application.__dict__)
		data.update({
			'application': application, 
			'options': application.params,
			'nodes': nodes,
			'domains': domains,
		})
		for node in nodes:
			print '%-30s' % application.name, node.name
			

def add(*args):
	node = env.node 
	if not args:
		for app in Application.objects.all():
			if not Proxy.objects.filter(name=app.name):
				Proxy.objects.get_or_create(node=node, name=app.name)
		manage('proxy dump')
		return 
	for pattern in args:
		Proxy.objects.get_or_create(node=node, name=pattern)
		manage('proxy dump %s' % name)

def dump(*args):
	node = env.node 
	proxies = Proxy.objects.filter(node=node)
	if args:
		if not '--all' in args:
			proxies = proxies.filter(name__in=args)
	for proxy in proxies:
		applications = Application.objects.filter(name=proxy.name)
		if not applications:
			continue
		nodes = Node.objects.filter(application__in=applications)
		domains = Alias.objects.filter(application__in=applications)
		application = applications[0]
		
		data = dict(application.__dict__)
		data.update({
			'application': application, 
			'options': application.params,
			'nodes': nodes,
			'domains': domains,
		})
		install_template(node, 
			template = 'reverseproxies/app', 
			context=data)
	install_template(node, 
		template = 'reverseproxies/commit')
		
