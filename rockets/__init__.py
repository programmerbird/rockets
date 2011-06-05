#!/usr/bin/env python
#-*- coding:utf-8 -*-


# BEGIN GIT POSTCOMMIT #################################
VERSION=""
# END GIT POSTCOMMIT ###################################

from rocket import services as services
from rocket import models as models
from rocket import loaders as loaders
from rocket import conf as conf

def get_path():
	import os
	return os.path.abspath(os.path.dirname(__file__))



