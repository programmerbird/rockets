#-*- coding:utf-8 -*-
from fabric.api import *

env.roledefs = {
	'test': ['127.0.0.1',],
}

def bootstrap():
	local('virtualenv --no-site-packages env', capture=False)
	local('env/bin/pip install -r requirements.ini', capture=False)

