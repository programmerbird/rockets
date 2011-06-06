# Django settings for manager project.
import os 

DEBUG = True
TEMPLATE_DEBUG = DEBUG


SECRET_KEY = 'g90oijlm43dsf,.m3wbkr3&hv41ib@qk1+*y8gf*epupqqyfzf'
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SERVER_DUMP_PATH = PROJECT_ROOT
ADMIN_USER = 'bird'

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'rockets.rocket',
    'rockets.boatyard',
    'rockets.git',
    'rockets.hostings',
    'rockets.ssh',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': os.path.join(PROJECT_ROOT, '.datastore'),                      
    }
}

