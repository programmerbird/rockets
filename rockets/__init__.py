#!/usr/bin/env python
#-*- coding:utf-8 -*-


# BEGIN GIT POSTCOMMIT #################################
VERSION="r2-1-gaad8d93"
# END GIT POSTCOMMIT ###################################

from rocket import services as services
from rocket import models as models
from rocket import loaders as loaders

def get_path():
	import os
	return os.path.abspath(os.path.dirname(__file__))



