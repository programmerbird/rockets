#-*- coding:utf-8 -*-


from rockets.servers.api import *
def main(*args):
	local('ssh %(user)s@%(host)s' % env, capture=False)
