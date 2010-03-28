#-*- coding:utf-8 -*-
from django.core.management import *
from django.db.models import get_apps
import os 

COMMON_ARGS = (
	('HANDLE_ARGS', lambda x : False),
	('NEED_INSTALLED', lambda x : hasattr(x, 'install')),
)

SERVICES = [
	#('name', 'module.path', {'HANDLE_ARGS': True}),
]

def get_app_services(app):
	result = []
	handles = []
	services_path = os.path.join(os.path.dirname(app.__file__), 'services')
	if os.path.exists(services_path):
		for file_name in os.listdir(services_path):
			if file_name.endswith('~'):
				continue
			if file_name.startswith('__'):
				continue
			if not (file_name.endswith('.pyc') or file_name.endswith('.py')):
				continue 
			service_name = file_name.rsplit('.', 1)[0]
			if service_name in handles:
				continue 
			handles.append(service_name)
			service_def = app.__package__ + '.services.' + service_name
			service = load_module(service_def)
			opts = dict([ (x, getattr(service, x, default(service) )) for (x, default) in COMMON_ARGS ])
			result.append( (service_name, service_def, opts), )
	return result
		
	
def get_services():
	global SERVICES
	if SERVICES:
		return SERVICES
	else:
		result = []
		for app in get_apps():
			app_services = get_app_services(app)
			if app_services:
				for service in app_services:
					result.append(service)
		SERVICES = result 
		return result


def load_module(definition):
	module = __import__(definition)	
	components = definition.split('.')
	for component in components[1:]:
		module = getattr(module, component)
	return module

class ServiceNotInstalled(CommandError):
	pass 
	
class ServiceNotFound(CommandError):
	pass 
	
def get_service(name):
	for (service_name, path, options) in get_services():
		if name != service_name:
			continue
		service = load_module(path) 
		for k,v in options.items():
			setattr(service, k, v)
		return service 		
	raise ServiceNotFound("service [%s] not found" % name)

			
def dispatch_service(service_name, args):
	service = get_service(service_name)
	args = args[2:]
	
	if service.NEED_INSTALLED:
		from rockets.servers.models import Node 
		from django.utils import simplejson
		node = Node.current()
		if service_name not in node.get_services():
			raise ServiceNotInstalled("[%s] did not installed [%s]" % (node.name, service_name))
	from api import connect
	connect()
			
	if args:
		subcommand = args[0]
		if hasattr(service, subcommand):
			args = args[1:]
		else:
			subcommand = 'main'
		if not hasattr(service, subcommand):
			print service.__doc__
			return
	return getattr(service, subcommand)(*args)
	
class ServerManagementUtility(ManagementUtility):
	"""
	Encapsulates the logic of the django-admin.py and manage.py utilities.

	A ManagementUtility has a number of commands, which can be manipulated
	by editing the self.commands dictionary.
	"""

	def fetch_command(self, subcommand):
		"""
		Tries to fetch the given subcommand, printing a message with the
		appropriate command called from the command line (usually
		"django-admin.py" or "manage.py") if it can't be found.
		"""
		app_name = get_commands()[subcommand]
		if isinstance(app_name, BaseCommand):
			# If the command is already loaded, use it directly.
			klass = app_name
		else:
			klass = load_command_class(app_name, subcommand)
		return klass

	def execute(self):
		"""
		Given the command-line arguments, this figures out which subcommand is
		being run, creates a parser appropriate to that command, and runs it.
		"""
		# Preprocess options to extract --settings and --pythonpath.
		# These options could affect the commands that are available, so they
		# must be processed early.
		parser = LaxOptionParser(usage="%prog subcommand [options] [args]",
								 version=get_version(),
								 option_list=BaseCommand.option_list)
		try:
			options, args = parser.parse_args(self.argv)
			handle_default_options(options)
		except:
			pass # Ignore any option errors at this point.
		
		try:
			subcommand = self.argv[1]
		except IndexError:
			sys.stderr.write("Type '%s help' for usage.\n" % self.prog_name)
			sys.exit(1)

		if subcommand == 'help':
			if len(args) > 2:
				self.fetch_command(args[2]).print_help(self.prog_name, args[2])
			else:
				parser.print_lax_help()
				sys.stderr.write(self.main_help_text() + '\n')
				sys.exit(1)
				
		# Special-cases: We want 'django-admin.py --version' and
		# 'django-admin.py --help' to work, for backwards compatibility.
		elif self.argv[1:] == ['--version']:
			# LaxOptionParser already takes care of printing the version.
			pass
		elif self.argv[1:] == ['--help']:
			parser.print_lax_help()
			sys.stderr.write(self.main_help_text() + '\n')
		else:
			try:
				self.fetch_command(subcommand).run_from_argv(self.argv)
			except KeyError:
				dispatch_service(subcommand, self.argv)
			except:
				import traceback
				traceback.print_exc()
				
def execute_from_command():
	try:
		from rocket.servers.utils import ServerManagementUtility
		utility = ServerManagementUtility()
		utility.execute()
	except Exception, e:	
		print e
		sys.exit(1)
	sys.exit(0)


