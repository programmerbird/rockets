# Django settings for manager project.
import os 

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
SECRET_KEY = '{{secret}}'

SERVER_DUMP_PATH = os.path.abspath(os.path.dirname(__file__))
DATABASE_NAME = os.path.abspath(os.path.join(os.path.dirname(__file__), '.datastore'))
ADMIN_USER = '{{user}}'
STORE_ROOT_PASSWORD = True
INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'rockets.rocket',
    'rockets.boatyard',
    'rockets.git',
    'rockets.hostings',
    'rockets.ssh',
)

