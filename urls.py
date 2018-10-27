from django.conf.urls import patterns
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = patterns('django.views.generic.simple',
                       (r'^$', RedirectView.as_view(url=reverse_lazy('userman2.views.users.displayUsers'), permanent=True))
                       )

urlpatterns += patterns('userman2.views.users',
                        (r'^adduser/$', 'addUser'),
                        (r'^users/$', 'displayUsers'),
                        (r'^users/([a-zA-Z][a-zA-Z\d\-_]+)/$', 'displayUser'),
                        (r'^users/([a-zA-Z][a-zA-Z\d\-_]+)/chfn/$', 'userChfn'),
                        (r'^users/([a-zA-Z][a-zA-Z\d\-_]+)/chdesc/$', 'userChdesc'),
                        (r'^users/([a-zA-Z][a-zA-Z\d\-_]+)/chwarnrm/$', 'userChwarnRm'),
                        (r'^users/([a-zA-Z][a-zA-Z\d\-_]+)/chsh/$', 'userChsh'),
                        (r'^users/([a-zA-Z][a-zA-Z\d\-_]+)/chpriv/$', 'userChpriv'),
                        (r'^users/([a-zA-Z][a-zA-Z\d\-_]+)/chpriv/rm/([a-zA-z]+)@([a-zA-z0-9-]+)/$', 'userRmpriv'),
                        (r'^users/([a-zA-Z][a-zA-Z\d\-_]+)/chgroup/$', 'userChgroup'),
                        (r'^users/([a-zA-Z][a-zA-Z\d\-_]+)/showldif/$', 'userShowldif'),
                        (r'^users/([a-zA-Z][a-zA-Z\d\-_]+)/chhomeank/$', 'chHomeAnk'),
                        (r'^users/([a-zA-Z][a-zA-Z\d\-_]+)/chhomech/$', 'chHomeCH'),
                        (r'^users/([a-zA-Z][a-zA-Z\d\-_]+)/resetpasswd/$', 'resetPassword'),
                        (r'^users/([a-zA-Z][a-zA-Z\d\-_]+)/chpasswd/$', 'chPassword'),
                        (r'^users/([a-zA-Z][a-zA-Z\d\-_]+)/removeprofile/$', 'removeProfile'),
                        (r'^users/([a-zA-Z][a-zA-Z\d\-_]+)/rm/$', 'rmUser'),
                        )

urlpatterns += patterns('userman2.views.massmail',
                        (r'^massmail/$', 'selectUsers'),
                        (r'^massmail/writemail/$', 'writeMail'),
                        (r'^massmail/writemail/sendmail/$', 'sendMail'),
                        )

urlpatterns += patterns('userman2.views.groups',
                        (r'^addgroup/([a-zA-Z\d]+)/$', 'addGroup'),
                        (r'^groups/$', 'displayGroups'),
                        (r'^groups/([a-zA-Z][a-zA-Z\d\-_]+)/$', 'displayGroup'),
                        (r'^groups/([a-zA-Z][a-zA-Z\d\-_]+)/rm/$', 'rmGroup'),
                        (r'^groups/([a-zA-Z][a-zA-Z\d\-_]+)/rmuser/([a-zA-Z][a-zA-Z\d_-]+)/$', 'rmuser'),
                        (r'^groups/([a-zA-Z][a-zA-Z\d\-_]+)/adduser/$', 'adduser'),
                        )

urlpatterns += patterns('userman2.views.aliases',
                        (r'^addalias/([a-zA-Z][a-zA-Z\-_\d.]+)/$', 'addAlias'),
                        (r'^aliases/$', 'displayAliases'),
                        (r'^aliases/([a-zA-Z][a-zA-Z\-_\d.]+)/$', 'displayAlias'),
                        (r'^aliases/([a-zA-Z][a-zA-Z\-_\d.]+)/rm/$', 'rmAlias'),
                        (r'^aliases/([a-zA-Z][a-zA-Z\-_\d.]+)/rmuser/([a-zA-Z\d][-+_\@\.a-zA-Z\d]+)/$', 'rmuser'),
                        (r'^aliases/([a-zA-Z][a-zA-Z\-_\d.]+)/adduser/$', 'adduser'),
                        )

urlpatterns += patterns('userman2.views.computers',
                        (r'^addcomputer/$', 'addComputer'),
                        (r'^computers/$', 'displayComputers'),
                        (r'^computers/([a-zA-Z][a-zA-Z\-_\d.]+\$)/rm/$', 'rmComputer'),
                        )
