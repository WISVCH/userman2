from django.conf.urls.defaults import *
from django.conf import settings

#from userman_web.views import users
urlpatterns = patterns('',
    # Example:
    # (r'^userman_web/', include('userman_web.foo.urls')),
    (r'^users/$', 'userman.views.users.displayUsers'),
    (r'^users/([a-zA-Z][a-zA-Z\d]+)/$', 'userman.views.users.displayUser'),
    (r'^users/([a-zA-Z][a-zA-Z\d]+)/chfn/$', 'userman.views.users.userChfn'),
    (r'^users/([a-zA-Z][a-zA-Z\d]+)/chdesc/$', 'userman.views.users.userChdesc'),
    (r'^users/([a-zA-Z][a-zA-Z\d]+)/chsh/$', 'userman.views.users.userChsh'),
    (r'^users/([a-zA-Z][a-zA-Z\d]+)/chpriv/$', 'userman.views.users.userChpriv'),
    (r'^users/([a-zA-Z][a-zA-Z\d]+)/chpriv/rm/([a-zA-z]+)@([a-zA-z]+)/$', 'userman.views.users.userRmpriv'),
    (r'^users/([a-zA-Z][a-zA-Z\d]+)/chgroup/$', 'userman.views.users.userChgroup'),
    (r'^users/([a-zA-Z][a-zA-Z\d]+)/showldif/$', 'userman.views.users.userShowldif'),
		
    (r'^groups/$', 'userman.views.groups.displayGroups'),
    (r'^groups/([a-zA-Z][a-zA-Z\d]+)/$', 'userman.views.groups.displayGroup'),
    (r'^groups/([a-zA-Z][a-zA-Z\d]+)/rm/$', 'userman.views.groups.rmgroup'),
    (r'^groups/([a-zA-Z][a-zA-Z\d]+)/rmuser/([a-zA-Z][a-zA-Z\d]+)/$', 'userman.views.groups.rmuser'),
    (r'^groups/([a-zA-Z][a-zA-Z\d]+)/adduser/$', 'userman.views.groups.adduser'),

    (r'^addalias/([a-zA-Z\d]+)/$', 'userman.views.aliases.addAlias'),
    (r'^aliases/$', 'userman.views.aliases.displayAliases'),
    (r'^aliases/([a-zA-Z][a-zA-Z_\d]+)/$', 'userman.views.aliases.displayAlias'),
    (r'^aliases/([a-zA-Z][a-zA-Z_\d]+)/rm/$', 'userman.views.aliases.rmAlias'),
    (r'^aliases/([a-zA-Z][a-zA-Z_\d]+)/rmuser/([a-zA-Z][\@\.a-zA-Z\d]+)/$', 'userman.views.aliases.rmuser'),
    (r'^aliases/([a-zA-Z][a-zA-Z_\d]+)/adduser/$', 'userman.views.aliases.adduser'),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),
    )
