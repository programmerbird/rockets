#-*- coding:utf-8 -*-


import os 
from django.template import Template, Context


def read_file(path):
	f = open(path, 'r')
	try:
		return ''.join(f.readlines())
	finally:
		f.close()
		
def _clone_file(source, target, context):
	content = read_file(source)
	rendered_content = Template(content).render(context)
	ensure_path(os.path.dirname(target))
	f = open(target, 'w')
	try:
		f.write(rendered_content)
	finally:
		f.close()

def ensure_path(path):
	chunks = path.split(os.sep)
	for x in xrange(1,len(chunks)+1):
		p = os.sep.join(chunks[:x]) + os.sep
		if not os.path.exists(p):
			os.mkdir(p)
		
def clone(source, target, context={}):
	c = Context(context)
	render = lambda x : Template(x).render(c)
	change_root = lambda x : x.replace(source, target)
	
	if os.path.isfile(source):
		source_path = source
		target_path = render(change_root(source))
		_clone_file(source_path, target_path, context)
	else:
		for root, dirs, files in os.walk(source):
			for name in files:
				if name[-1:] in '~':
					continue
				source_path = os.path.join(root, name)
				target_path = render(change_root(source_path))
				_clone_file(source_path, target_path, c)
			for name in dirs:
				source_path = os.path.join(root, name)
				target_path = render(change_root(source_path))
				if not os.path.exists(target_path):
					ensure_path(target_path)
			

