#-*- coding:utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from rockets.servers.api import *

class UsageError(CommandError):
	def __init__(self, txt):
		super(UsageError, self).__init__("Usage: boatyard aptitude " + txt)


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		connect()
		run('aptitude -y ' + ' '.join(args), pty=True)

