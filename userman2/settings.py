# Django settings for userman2 project.
import os
import time

ADMINS = (
    ('Beheer', 'beheer@ch.tudelft.nl'),
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

# Absolute path to the directory static files should be collected to.
STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../static/')

# URL prefix for static files.
STATIC_URL = '/static/'

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

MIDDLEWARE = (
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django_request_logger.middleware.StoreRequestMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(os.path.dirname(__file__), 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ]
        }
    },
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_request_logger',
    'userman2',
)

ALLOWED_HOSTS = [
    '127.0.0.1',
]

EMAIL_HOST = 'ch.tudelft.nl'
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SSH_ANK_HOSTKEY = "AAAAC3NzaC1lZDI1NTE5AAAAIM6VQmPhRQAwOn1CpW8QMGnQI/UmLtTjh4Y8/aF1hngs"

LDAP_HOST = "ldaps://ank.chnet"
LDAP_USER = "cn=admin,dc=ank,dc=chnet"
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

ANK_HOME_BASE = '/export/gebruikers/' + time.strftime('%Y') + '/'
CH_HOME_BASE = '/home/' + time.strftime('%Y') + '/'
DEFAULT_SHELL = '/bin/bash'
GRAVEYARD_DIR = '/var/local/graveyard/'
ADMIN_MAIL = 'pccom@ch.tudelft.nl'

ROOT_PATH = os.path.dirname(__file__)

from .local import *
