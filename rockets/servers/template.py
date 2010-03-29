#-*- coding:utf-8 -*-


import os 
import re 
from path import *
				
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
	f.write('\n')
	f.write('RM=rm -f\n')
	f.write('RMDIR=rmdir --ignore-fail-on-non-empty\n')
	f.write('\n')
	for x in files:
		f.write('$RM "%s"\n' % x)
	f.write('\n')
	for x in dirs:
		f.write('$RMDIR "%s"\n' % x)
	f.close()
	
def dir_compare(a, b):
	if a.startswith(b):
		return -1
	elif b.startswith(a):
		return 1
	else:
		return cmp(a,b)
		
def uninstall_template(node, template, context={}):	
	path = get_server_dump_path(node)
	template_name = template.replace(os.sep, '_')
	template_path = find_template_path(template)

	script_dir = os.path.join(template_path, 'SCRIPTS')
	prerm_path = os.path.join(script_dir, 'prerm')
	postrm_path = os.path.join(script_dir, 'postrm')

	ensure_path(get_server_dump_path(node, 'SCRIPTS'))
	if os.path.exists(prerm_path):
		name = get_script_name(node, template_name + '_prerm')
		clone(prerm_path, get_server_dump_path(node, 'SCRIPTS', name), context=context)

	dirs, files = get_clone_files(template_path, path, context=context, ignore_dirs=[script_dir])
	files = [ x[len(path):] for x in files ]
	dirs = [ x[len(path):] for x in dirs ]
	dirs.sort(cmp=dir_compare)
	
	# remove dump files
	for x in files:
		try:
			os.remove(get_server_dump_path(node, x[1:]))
		except OSError:
			pass 
	for x in dirs:
		try:
			os.rmdir(get_server_dump_path(node, x[1:]))
		except OSError:
			pass 
	
	name = get_script_name(node, template_name + '_rm')	
	f = open(get_server_dump_path(node, 'SCRIPTS', name), 'w')
	try:
		make_uninstall_script(f, dirs, files)
	finally:
		f.close()
		
	if os.path.exists(postrm_path):
		name = get_script_name(node, template_name + '_postrm')
		clone(postrm_path, get_server_dump_path(node, 'SCRIPTS', name), context=context)

