from django.conf.urls.defaults import *
from django.conf import settings

#from userman_web.views import users
urlpatterns = patterns('',
    # Example:
    # (r'^userman_web/', include('userman_web.foo.urls')),
    (r'^users/$', 'views.users.displayUsers'),
    (r'^users/([a-zA-Z][a-zA-Z\d]+)/$', 'views.users.displayUser'),
    (r'^users/([a-zA-Z][a-zA-Z\d]+)/chfn/$', 'views.users.userChfn'),
    (r'^users/([a-zA-Z][a-zA-Z\d]+)/chdesc/$', 'views.users.userChdesc'),
    (r'^users/([a-zA-Z][a-zA-Z\d]+)/chsh/$', 'views.users.userChsh'),
    (r'^users/([a-zA-Z][a-zA-Z\d]+)/chgroup/$', 'views.users.userChgroup'),
		
    (r'^groups/$', 'views.groups.displayGroups'),
    (r'^groups/([a-zA-Z][a-zA-Z\d]+)/$', 'views.groups.displayGroup'),


    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/adriaan/userman/userman_web/media'}),
    )
