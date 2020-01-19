from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.generic import RedirectView
import userman2.views.aliases as aliases
import userman2.views.groups as groups
import userman2.views.users as users

urlpatterns = [
    url(r"^$", RedirectView.as_view(url=reverse_lazy(users.displayUsers), permanent=True)),
    url(r"^users/$", RedirectView.as_view(url=reverse_lazy(users.displayUsers), permanent=True)),
]

urlpatterns += [
    url(r"^adduser$", users.addUser, name="addUser"),
    url(r"^users$", users.displayUsers, name="displayUsers"),
    url(r"^users.json$", users.getUsersJson),
    url(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)$", users.displayUser, name="displayUser"),
    url(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/dienst2status.json$", users.getUserDienst2Status),
    url(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/chfn$", users.userChfn),
    url(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/chdesc$", users.userChdesc),
    url(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/chwarnrm$", users.userChwarnRm),
    url(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/chsh$", users.userChsh),
    url(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/chpriv$", users.userChpriv),
    url(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/chpriv/rm/([a-zA-z-]+)@([a-zA-z\d-]+)$", users.userRmpriv),
    url(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/chgroup$", users.userChgroup),
    url(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/chhomeank$", users.chHomeAnk),
    url(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/chhomech$", users.chHomeCH),
    url(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/resetpasswd.json$", users.resetPassword),
    url(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/rm$", users.rmUser),
]

urlpatterns += [
    url(r"^groups$", groups.displayGroups, name="displayGroups"),
    url(r"^groups/([a-zA-Z\d]+)/add$", groups.addGroup),
    url(r"^groups/([a-zA-Z][a-zA-Z\d\-_]+)$", groups.displayGroup, name="displayGroup"),
    url(r"^groups/([a-zA-Z][a-zA-Z\d\-_]+)/rm$", groups.rmGroup),
    url(r"^groups/([a-zA-Z][a-zA-Z\d\-_]+)/rmuser/([a-zA-Z][a-zA-Z\d_-]+)$", groups.rmuser),
    url(r"^groups/([a-zA-Z][a-zA-Z\d\-_]+)/adduser$", groups.adduser),
]

urlpatterns += [
    url(r"^aliases$", aliases.displayAliases, name="displayAliases"),
    url(r"^aliases/([a-zA-Z][a-zA-Z\-_\d.]+)/add$", aliases.addAlias),
    url(r"^aliases/([a-zA-Z][a-zA-Z\-_\d.]+)$", aliases.displayAlias, name="displayAlias"),
    url(r"^aliases/([a-zA-Z][a-zA-Z\-_\d.]+)/rm$", aliases.rmAlias),
    url(r"^aliases/([a-zA-Z][a-zA-Z\-_\d.]+)/rmuser/([a-zA-Z\d][-+_\@\.a-zA-Z\d]+)$", aliases.rmuser),
    url(r"^aliases/([a-zA-Z][a-zA-Z\-_\d.]+)/adduser$", aliases.adduser),
]
