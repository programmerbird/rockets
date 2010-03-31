#-*- coding:utf-8 -*-

import os
from rockets.servers.api import *
from rockets.servers.path import get_server_dump_path
from fabric.contrib.console import confirm

def main(*args):
	node = env.node
	print node 
	print "%-15s : %s" % ('user', node.username)
	for ip in node.get_public_ip():
		print "%-15s : %s" % ('public ip', ip)
	for ip in node.get_private_ip():
		print "%-15s : %s" % ('private ip', ip)
	
