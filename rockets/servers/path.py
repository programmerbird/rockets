#-*- coding:utf-8 -*-


import os 
import re 
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

	files = []
	dirs = []
	if os.path.isfile(source):
		source_path = source
		target_path = render(change_root(source))
		os.remove(target_path)
		files.append(target_path)
	else:
		for root, dirs, files in os.walk(source):
			if root in ignore_dirs:
				continue
			for name in files:
				if name.endswith('~'):
					continue
				source_path = os.path.join(root, name)
				target_path = render(change_root(source_path))
				try:
					os.remove(target_path)
				except OSError:
					pass
				files.append(target_path)
				
		for root, dirs, files in os.walk(source):
			if root in ignore_dirs:
				continue
			for name in dirs:
				source_path = os.path.join(root, name)
				if source_path in ignore_dirs:
					continue
				target_path = render(change_root(source_path))
				if os.path.exists(target_path):
					try:
						os.rmdir(target_path)
					except OSError:
						pass 
					dirs.append(target_path)
	return dirs, files 

def get_server_dump_path(node, *args):
	from django.conf import settings 
	SERVER_DUMP_PATH = getattr(settings, 'SERVER_DUMP_PATH')
	return os.path.abspath(os.path.join(SERVER_DUMP_PATH, node.name, *args))

NUMBER_PATTERN = re.compile(r'^(\d+)\-')
def get_script_name(node, script_name):
	path = get_server_dump_path(node, 'SCRIPTS')
	max_number = 0
	for x in os.listdir(path):
		matches = NUMBER_PATTERN.match(x)
		if matches:
			number = int(matches.group(1))
			max_number = max(number+1, max_number)
	return '%0.4d-%s' % (max_number, script_name)
				
def find_template_path(path):
	from django.template.loaders.app_directories import app_template_dirs
	from django.template import TemplateDoesNotExist
	for x in app_template_dirs:
		file_path = os.path.join(x, path)
		if os.path.exists(file_path):
			return file_path 
	raise TemplateDoesNotExist
	
def install_template(node, template, context={}):
	path = get_server_dump_path(node)
	template_name = template.replace(os.sep, '_')
	template_path = find_template_path(template)
	
	script_dir = os.path.join(template_path, 'SCRIPTS')
	postinst_path = os.path.join(script_dir, 'postinst')
	
	clone(template_path, path, context=context, ignore_dirs = [script_dir])
	if os.path.exists(postinst_path):
		ensure_path(get_server_dump_path(node, 'SCRIPTS'))
		name = get_script_name(node, template_name + '_postinst')
		clone(postinst_path, get_server_dump_path(node, 'SCRIPTS', name), context=context)

def make_uninstall_script(outfile, dirs, files):
	f = outfile
	f.write('#!/bin/bash\n')
	f.write('RM=rm -f\n')
	f.write('RMDIR=rmdir --ignore-fail-on-non-empty\n')
	f.write('\n')
	for x in files:
		f.write('$RM -f "%s"\n' % x)
	for x in dirs:
		f.write('$RMDIR "%s"\n' % x)
	f.close()
	
def uninstall_template(node, template):	
	path = get_server_dump_path(node)
	template_name = template.replace(os.sep, '_')
	template_path = find_template_path(template)

	script_dir = os.path.join(template_path, 'SCRIPTS')
	prerm_path = os.path.join(script_dir, 'prerm')

	ensure_path(get_server_dump_path(node, 'SCRIPTS'))
	if os.path.exists(prerm_path):
		name = get_script_name(node, template_name + '_prerm')
		clone(prerm_path, get_server_dump_path(node, 'SCRIPTS', name), context=context)

	dirs, files = get_clone_files(template_path, source, context=context, ignore_dirs=[script_dir])
	name = get_script_name(node, template_name + '_rm')	
	f = open(get_server_dump_path(node, 'SCRIPTS', name), 'w')
	try:
		make_uninstall_script(f, dirs, files)
	finally:
		f.close()

