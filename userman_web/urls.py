from django.conf.urls.defaults import *
from django.conf import settings

#from userman_web.views import users
urlpatterns = patterns('userman.views.users',
    (r'^userman2/adduser/$', 'addUser'),
    (r'^userman2/users/$', 'displayUsers'),
    (r'^userman2/users/([a-zA-Z][a-zA-Z\d\-_]+)/$', 'displayUser'),
    (r'^userman2/users/([a-zA-Z][a-zA-Z\d\-_]+)/chfn/$', 'userChfn'),
    (r'^userman2/users/([a-zA-Z][a-zA-Z\d\-_]+)/chdesc/$', 'userChdesc'),
    (r'^userman2/users/([a-zA-Z][a-zA-Z\d\-_]+)/chwarnrm/$', 'userChwarnRm'),
    (r'^userman2/users/([a-zA-Z][a-zA-Z\d\-_]+)/chsh/$', 'userChsh'),
    (r'^userman2/users/([a-zA-Z][a-zA-Z\d\-_]+)/chpriv/$', 'userChpriv'),
    (r'^userman2/users/([a-zA-Z][a-zA-Z\d\-_]+)/chpriv/rm/([a-zA-z]+)@([a-zA-z]+)/$', 'userRmpriv'),
    (r'^userman2/users/([a-zA-Z][a-zA-Z\d\-_]+)/chgroup/$', 'userChgroup'),
    (r'^userman2/users/([a-zA-Z][a-zA-Z\d\-_]+)/showldif/$', 'userShowldif'),
    (r'^userman2/users/([a-zA-Z][a-zA-Z\d\-_]+)/chhomeank/$', 'chHomeAnk'),
    (r'^userman2/users/([a-zA-Z][a-zA-Z\d\-_]+)/chhomech/$', 'chHomeCH'),
    (r'^userman2/users/([a-zA-Z][a-zA-Z\d\-_]+)/resetpasswd/$', 'resetPassword'),
    (r'^userman2/users/([a-zA-Z][a-zA-Z\d\-_]+)/chpasswd/$', 'chPassword'),
    (r'^userman2/users/([a-zA-Z][a-zA-Z\d\-_]+)/genloginscript/$', 'genLoginScript'),
    (r'^userman2/users/([a-zA-Z][a-zA-Z\d\-_]+)/removeprofile/$', 'removeProfile'),
    (r'^userman2/users/([a-zA-Z][a-zA-Z\d\-_]+)/rm/$', 'rmUser'),
)

urlpatterns += patterns('userman.views.massmail',
    (r'^userman2/massmail/$', 'selectUsers'),
    (r'^userman2/massmail/writemail/$', 'writeMail'),
    (r'^userman2/massmail/writemail/sendmail/$', 'sendMail'),
)

urlpatterns += patterns('userman.views.groups',
    (r'^userman2/addgroup/([a-zA-Z\d]+)/$', 'addGroup'),
    (r'^userman2/groups/$', 'displayGroups'),
    (r'^userman2/groups/([a-zA-Z][a-zA-Z\d\-_]+)/$', 'displayGroup'),
    (r'^userman2/groups/([a-zA-Z][a-zA-Z\d\-_]+)/rm/$', 'rmGroup'),
    (r'^userman2/groups/([a-zA-Z][a-zA-Z\d\-_]+)/rmuser/([a-zA-Z][a-zA-Z\d_-]+)/$', 'rmuser'),
    (r'^userman2/groups/([a-zA-Z][a-zA-Z\d\-_]+)/adduser/$', 'adduser'),
)
urlpatterns += patterns('userman.views.aliases',
    (r'^userman2/addalias/([a-zA-Z][a-zA-Z\-_\d.]+)/$', 'addAlias'),
    (r'^userman2/aliases/$', 'displayAliases'),
    (r'^userman2/aliases/([a-zA-Z][a-zA-Z\-_\d.]+)/$', 'displayAlias'),
    (r'^userman2/aliases/([a-zA-Z][a-zA-Z\-_\d.]+)/rm/$', 'rmAlias'),
    (r'^userman2/aliases/([a-zA-Z][a-zA-Z\-_\d.]+)/rmuser/([a-zA-Z\d][-+_\@\.a-zA-Z\d]+)/$', 'rmuser'),
    (r'^userman2/aliases/([a-zA-Z][a-zA-Z\-_\d.]+)/adduser/$', 'adduser'),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}), )
