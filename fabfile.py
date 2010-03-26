
from fabric.api import *

env.hosts = ['127.0.0.1']

def bootstrap():
	local('virtualenv --no-site-packages env', capture=False)
	local('env/bin/pip install -r requirements.ini', capture=False)
	local('cp bin/* env/bin/')
	local('rocket syncdb')

