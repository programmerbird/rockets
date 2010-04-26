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
	if source.endswith('pyc'):
		return
	print "->", target
	content = read_file(source)
	rendered_content = Template(unicode(content)).render(context)
	ensure_path(os.path.dirname(target))
	f = open(target, 'w')
	try:
		f.write(unicode(rendered_content))
	finally:
		f.close()

def ensure_path(path):
	chunks = path.split(os.sep)
	for x in xrange(1,len(chunks)+1):
		p = os.sep.join(chunks[:x]) + os.sep
		if not os.path.exists(p):
			os.mkdir(p)
		
def clone(source, target, context={}, ignore_dirs=[]):
	c = Context(context)
	render = lambda x : Template(x).render(c)
	change_root = lambda x : x.replace(source, target)
	
	if os.path.isfile(source):
		source_path = source
		target_path = render(change_root(source))
		_clone_file(source_path, target_path, c)
	else:
		for root, dirs, files in os.walk(source):
			if root in ignore_dirs:
				continue
			for name in files:
				if name.endswith('~'):
					continue
				source_path = os.path.join(root, name)
				target_path = render(change_root(source_path))
				_clone_file(source_path, target_path, c)
			for name in dirs:
				source_path = os.path.join(root, name)
				if source_path in ignore_dirs:
					continue
				target_path = render(change_root(source_path))
				if not os.path.exists(target_path):
					ensure_path(target_path)
			
def get_clone_files(source, target, context={}, ignore_dirs=[]):
	c = Context(context)
	render = lambda x : Template(x).render(c)
	change_root = lambda x : x.replace(source, target)

	result_files = []
	result_dirs = []
	if os.path.isfile(source):
		source_path = source
		target_path = render(change_root(source))
		result_files.append(target_path)
	else:
		for root, dirs, files in os.walk(source):
			if root in ignore_dirs:
				continue
			for name in files:
				if name.endswith('~'):
					continue
				source_path = os.path.join(root, name)
				target_path = render(change_root(source_path))
				result_files.append(target_path)
				
		for root, dirs, files in os.walk(source):
			if root in ignore_dirs:
				continue
			for name in dirs:
				source_path = os.path.join(root, name)
				if source_path in ignore_dirs:
					continue
				target_path = render(change_root(source_path))
				if os.path.exists(target_path):
					result_dirs.append(target_path)
	return result_dirs, result_files 

def get_server_dump_path(node, *args):
	from django.conf import settings 
	SERVER_DUMP_PATH = getattr(settings, 'SERVER_DUMP_PATH')
	return os.path.abspath(os.path.join(SERVER_DUMP_PATH, node.name, *args))

