#!/usr/bin/env python
#-*- coding:utf-8 -*-



import os, re 
import conf
from django.conf import settings
from django.template import Template, Context

SYMLINK_SUFFIX = getattr(settings, 'SYMLINK_SUFFIX', '->')
EXTENDFILE_SUFFIX = getattr(settings, 'EXTENDFILE_SUFFIX', '.e')

def read_file(path):
	f = open(path, 'r')
	try:
		return ''.join(f.readlines())
	finally:
		f.close()
		
def ensure_path(path):
	chunks = path.split(os.sep)
	for x in xrange(1,len(chunks)+1):
		p = os.sep.join(chunks[:x]) + os.sep
		if not os.path.exists(p):
			os.mkdir(p)
			
def is_ignore_file(filename):
	if unicode(filename).endswith('~'):
		return True
	if unicode(filename).endswith('pyc'):
		return True
	if unicode(filename)=='.gitignore':
		return True
	return False
	
def travel(source, target, context={}, ignore_dirs=[], action=None):
	if not os.path.exists(source):
		return 
		
	template_context = Context(context)
	render = lambda x : Template(x).render(template_context)
	change_root = lambda x : x.replace(source, target)
	
	if os.path.isfile(source):
		source_path = source
		target_path = render(target)
		action(source_path, target_path)
	else:
		for root, dirs, files in os.walk(source):
			if root in ignore_dirs:
				continue
			for name in dirs:
				source_path = os.path.join(root, name)
				is_ignore = False
				for ignore_dir in ignore_dirs:
					if source_path.startswith(ignore_dir):
						is_ignore = True
						break
				if is_ignore:
					continue
				target_path = render(change_root(source_path))
				ensure_path(target_path)
				action(source_path, target_path)
			for name in files:
				if is_ignore_file(name):
					continue
				source_path = os.path.join(root, name)
				is_ignore = False
				for ignore_dir in ignore_dirs:
					if source_path.startswith(ignore_dir):
						is_ignore = True
						break
				if is_ignore:
					continue
				target_path = render(change_root(source_path))
				action(source_path, target_path)

def dump(source, target, context={}, ignore_dirs=[], debug=None):
	template_context = Context(context)
	def dump_file(source, target):
		if not os.path.isfile(source):
			return 
		if is_ignore_file(source):
			return 
		if source.endswith(SYMLINK_SUFFIX):
			return
		if debug:
			debug(target)
		content = read_file(source)
		rendered_content = Template(unicode(content)).render(template_context)
			
		ensure_path(os.path.dirname(target))
		f = open(target, 'w')
		try:
			f.write(unicode(rendered_content))
		finally:
			f.close()
			
	travel(source, target, 
		context=context, 
		ignore_dirs=ignore_dirs, 
		action=dump_file)
		
def get_files(source, target, context={}, ignore_dirs=[]):
	files = []
	dirs = []
	links = []
		
	template_context = Context(context)
	def add(source, target):
		if os.path.isfile(source):
			if source.endswith(SYMLINK_SUFFIX):
				content = read_file(source)
				rendered_content = Template(unicode(content)).render(template_context)
				links.append((rendered_content.strip(), target[:-len(SYMLINK_SUFFIX)]),)
			else:
				files.append(target)
		elif os.path.exists(source):
			dirs.append(target)
			
	travel(source, target, 
		context=context, 
		ignore_dirs=ignore_dirs, 
		action=add)
	return dirs, files, links

NUMBER_PATTERN = re.compile(r'^(\d+)\-')

def find_template_path(path):
	from django.template.loaders.app_directories import app_template_dirs
	from django.template import TemplateDoesNotExist
	for x in app_template_dirs:
		file_path = os.path.abspath(os.path.join(x, path))
		if os.path.exists(file_path):
			return file_path 
	raise TemplateDoesNotExist
	
class Dumper(object):
	def __init__(self, node, template):
		self.node = node 
		self.template = template 
		self.debug = None
	
		self.target_path = os.path.join(conf.SERVER_DUMP_PATH, self.node.name)
		self.template_name = self.template.replace(os.sep, '-')
		self.template_path = find_template_path(template)
		self.template_script_dir = os.path.join(self.template_path, 'SCRIPTS')
		self.template_plugin_dir = os.path.join(self.template_path, 'PLUGINS')
		self.target_script_dir = os.path.join(self.target_path, 'SCRIPTS')
		self.context = {}
		
	def get_script_name(self, script):
		result = 0
		if os.path.exists(self.target_script_dir):
			for x in os.listdir(self.target_script_dir):
				matches = NUMBER_PATTERN.match(x)
				if matches:
					number = int(matches.group(1))
					result = max(number+1, result) 
		return '%0.3d-%s' % (result, script)
		
	def script(self, script):
		base_name = os.path.basename(script)
		output = self.get_script_name(base_name)
		self.dump(
			os.path.join('SCRIPTS', script), 
			os.path.join('SCRIPTS', output))
			
	def dump(self, source=None, target=None):
		if not source:
			source = ''
		if not target:
			target = source 
		template_path = os.path.join(self.template_path, source)
		target_path = os.path.join(self.target_path, target)
		dump(template_path, target_path, context=self.context, debug=self.debug, 
			ignore_dirs=[self.template_plugin_dir, self.template_script_dir])
			
	def get_files(self, source=None, target=None):
		if not source:
			source = ''
		if not target:
			target = source 
			
		template_path = os.path.join(self.template_path, source)
		target_path = os.path.join(self.target_path, target)
		return get_files(template_path, target_path, context=self.context, 
			ignore_dirs=[self.template_plugin_dir, self.template_script_dir])
			
	def quickscan(self):
		dirs, files, links = self.get_files()
		prefix_length = len(self.target_path)
		dirs = [ x[prefix_length:] for x in dirs ]
		files = [ x[prefix_length:] for x in files ]
		links = [ (source, target[prefix_length:]) for source,target in links ]
		dirs.sort(cmp=_parent_dir_compare)
		self.context['rocket_dirs'] = dirs
		self.context['rocket_files'] = files 
		self.context['rocket_links'] = links
		self.context['rocket_efiles_suffix'] = EXTENDFILE_SUFFIX
		self.context['rocket_efiles'] = [ x[:-len(EXTENDFILE_SUFFIX)] for x in dirs if unicode(x).endswith(EXTENDFILE_SUFFIX) ]
		
		self.files = files 
		self.dirs = dirs
			
		
			
def _parent_dir_compare(a, b):
	if a.startswith(b):
		return 1
	elif b.startswith(a):
		return -1
	else:
		return cmp(a,b)
		
def install_template(node, template, context=None, debug=None):
	dumper = Dumper(node=node, template=template)
	dumper.context = context 
	dumper.debug = debug
	if not os.path.exists(dumper.template_path):
		return
	
	# get installed files + folders  
	dumper.quickscan()

	# preinst script 
	dumper.script('preinst')
	
	# dump
	dumper.dump()
	
	# inst script 
	dumper.script(find_template_path('rocket/inst.sh'))
	
	# post inst script 
	dumper.script('postinst')

def remove_template(node, template, context={}, debug=None):	
	dumper = Dumper(node=node, template=template)
	dumper.context = context 
	dumper.debug = debug
	if not os.path.exists(dumper.template_path):
		return
		
	# get installed files + folders  
	dumper.quickscan()
	
	# prerm script 
	dumper.script('prerm.sh')
	
	# remove links
	for x in dumper.links:
		try:
			os.remove(os.path.join(dumper.target_path, x[1:]))
		except OSError:
			pass 
	
	# remove dump files
	for x in dumper.files:
		try:
			os.remove(os.path.join(dumper.target_path, x[1:]))
		except OSError:
			pass 
			
	for x in dumper.dirs:
		try:
			os.rmdir(os.path.join(dumper.target_path, x[1:]))
		except OSError:
			pass 
	
	# rm script 
	dumper.script(find_template_path('rocket/rm.sh'))
	
	# postrm script
	dumper.script('postrm')
	
