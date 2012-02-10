# Django settings for userman2 project.
import os

ADMINS = (
    # ('PC.Com', 'adriaan@ch.tudelft.nl'),
)

MANAGERS = ADMINS

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
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = ''

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'userman2.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'userman2',
)

LDAP_HOST = 'ldaps://frans.chnet/'
LDAP_USER = 'cn=admin,dc=ank,dc=chnet'
LDAP_PASS = 'n0w|l8r'
LDAP_BASE = 'dc=ank,dc=chnet'
LDAP_ACTIONDN = 'ou=Actions,' + LDAP_BASE
LDAP_USERDN = 'ou=People,' + LDAP_BASE
LDAP_GROUPDN = 'ou=Group,' + LDAP_BASE
LDAP_COMPUTERDN = 'ou=Computers,' + LDAP_BASE
LDAP_ALIASDN = 'ou=Aliases,' + LDAP_BASE
MIN_GROUP_ID = 1000
MAX_GROUP_ID = 1500
MIN_COMPUTER_ID = 5000
MAX_COMPUTER_ID = 5500
MIN_USER_ID = 1500
MAX_USER_ID = 2500
MACHINE_GIDNUMBER = 1102
USER_GIDNUMBER = 100
import time
ANK_HOME_BASE = '/export/gebruikers/' + time.strftime('%Y') + '/'
CH_HOME_BASE = '/home/' + time.strftime('%Y') + '/'
DEFAULT_SHELL = '/bin/bash'
GRAVEYARD_DIR = '/var/local/graveyard/'
ADMIN_MAIL = 'pccom@ch.tudelft.nl'
USERMAN_PREFIX='/userman2'

from local import *