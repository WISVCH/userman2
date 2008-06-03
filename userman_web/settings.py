# Django settings for userman_web project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('PC.Com', 'adriaan@ch.tudelft.nl'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5)6_y^#_82@a=t3fu@2ttr(v#=93ng#q3vx@quj!=y-md^q1pn'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'userman_web.urls'

import os
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.getcwd(),'userman/templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'userman_web.userman',
)

LDAP_HOST = 'ldaps://frans.chnet/'
LDAP_USER = 'cn=admin,dc=ank,dc=chnet'
LDAP_PASS = 'n0w|l8r'
LDAP_BASE = 'dc=ank,dc=chnet'
LDAP_ACTIONDN = 'ou=Actions,' + LDAP_BASE
LDAP_USERDN = 'ou=People,' + LDAP_BASE
LDAP_GROUPDN = 'ou=Group,' + LDAP_BASE
LDAP_COMPUTERDN = 'ou=Machines,' + LDAP_BASE
LDAP_ALIASDN = 'ou=Aliases,' + LDAP_BASE
MIN_GROUP_ID = 1000
MAX_GROUP_ID = 1500
MIN_MACHINE_ID = 5000
MAX_MACHINE_ID = 5500
MIN_USER_ID = 1500
MAX_USER_ID = 2500
MACHINE_GIDNUMBER = 1102
USER_GIDNUMBER = 100
import time
ANK_HOME_BASE = '/export/gebruikers/' + time.strftime('%Y') + '/'
CH_HOME_BASE = '/home/' + time.strftime('%Y') + '/'
DEFAULT_SHELL = '/bin/bash'
GRAVEYARD_DIR = '/var/local/graveyard/'
ADMIN_MAIL = 'adriaan@ch.tudelft.nl'