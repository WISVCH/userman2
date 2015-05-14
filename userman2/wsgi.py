import os
import sys

path = '/srv/www/userman/'
if path not in sys.path:
    sys.path.append(path)
    sys.path.append(os.path.normpath(path + "/.."))

os.environ['DJANGO_SETTINGS_MODULE'] = 'userman.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
