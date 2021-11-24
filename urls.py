from django.urls import reverse_lazy, re_path, include
from django.views.generic import RedirectView

import userman2.views.actions as actions
import userman2.views.aliases as aliases
import userman2.views.groups as groups
import userman2.views.users as users

urlpatterns = [
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy(users.displayUsers), permanent=True)),
    re_path(r"^users/$", RedirectView.as_view(url=reverse_lazy(users.displayUsers), permanent=True)),
]

urlpatterns += [
    re_path(r"^adduser$", users.addUser, name="addUser"),
    re_path(r"^users$", users.displayUsers, name="displayUsers"),
    re_path(r"^users.json$", users.getUsersJson),
    re_path(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)$", users.displayUser, name="displayUser"),
    re_path(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/dienst2status.json$", users.getUserDienst2Status),
    re_path(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/chfn$", users.userChfn),
    re_path(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/chdesc$", users.userChdesc),
    re_path(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/chsh$", users.userChsh),
    re_path(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/chpriv$", users.userChpriv),
    re_path(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/chpriv/rm/([a-zA-z-]+)@([a-zA-z\d-]+)$", users.userRmpriv),
    re_path(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/chgroup$", users.userChgroup),
    re_path(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/resetpasswd.json$", users.resetPassword),
    re_path(r"^users/([a-zA-Z][a-zA-Z\d\-_]+)/rm$", users.rmUser),
]

urlpatterns += [
    re_path(r"^groups$", groups.displayGroups, name="displayGroups"),
    re_path(r"^groups/([a-zA-Z\d]+)/add$", groups.addGroup),
    re_path(r"^groups/([a-zA-Z][a-zA-Z\d\-_]+)$", groups.displayGroup, name="displayGroup"),
    re_path(r"^groups/([a-zA-Z][a-zA-Z\d\-_]+)/rm$", groups.rmGroup),
    re_path(r"^groups/([a-zA-Z][a-zA-Z\d\-_]+)/rmuser/([a-zA-Z][a-zA-Z\d_-]+)$", groups.rmuser),
    re_path(r"^groups/([a-zA-Z][a-zA-Z\d\-_]+)/adduser$", groups.adduser),
]

urlpatterns += [
    re_path(r"^aliases$", aliases.displayAliases, name="displayAliases"),
    re_path(r"^aliases/([a-zA-Z][a-zA-Z\-_\d.]+)/add$", aliases.addAlias),
    re_path(r"^aliases/([a-zA-Z][a-zA-Z\-_\d.]+)$", aliases.displayAlias, name="displayAlias"),
    re_path(r"^aliases/([a-zA-Z][a-zA-Z\-_\d.]+)/rm$", aliases.rmAlias),
    re_path(r"^aliases/([a-zA-Z][a-zA-Z\-_\d.]+)/rmuser/([a-zA-Z\d][-+_@.a-zA-Z\d]+)$", aliases.rmuser),
    re_path(r"^aliases/([a-zA-Z][a-zA-Z\-_\d.]+)/adduser$", aliases.adduser),
]

urlpatterns += [
    re_path("actions/actions.json", actions.getActions),
    re_path("actions", actions.displayActions, name="displayActions"),
]

# Health check
urlpatterns += [
    re_path("healthz", include("health_check.urls")),
]
