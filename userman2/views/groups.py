from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from userman2.forms.group import *
from userman2.model import group, action
from userman2.views.error import Error


def displayGroups(request):
    if request.GET:
        form = GroupsForm(request.GET)
        if form.is_valid():
            groups = group.GetAllGroups(form.cleaned_data)
        else:
            groups = group.GetAllGroups()
    else:
        form = GroupsForm()
        groups = group.GetAllGroups()

    return render(request, "groupsaliases.html", {"groups": groups, "form": form})


def displayGroup(request, cn):
    try:
        groupObj = group.FromCN(cn)
    except:
        raise Http404
    return render(request, "groupalias.html", {"group": groupObj})


def rmuser(request, cn, user):
    if request.method != "POST":
        raise Http404

    try:
        groupObj = group.FromCN(cn)
    except:
        raise Http404

    if not user in groupObj.members:
        raise Http404

    groupObj.connectRoot()
    groupObj.removeMember(user)
    return HttpResponseRedirect("/groups/" + groupObj.cn)


def adduser(request, cn):
    try:
        groupObj = group.FromCN(cn)
    except:
        raise Http404

    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            groupObj.connectRoot()
            groupObj.addMember(str(form.cleaned_data["user"]))
            return HttpResponseRedirect("/groups/" + groupObj.cn)
    else:
        form = AddUserForm()

    return render(request, "form.html", {"form": form, "uid": groupObj.cn})


def addGroup(request, parent):
    if not parent in group.GetParents():
        raise Http404

    if request.method == "POST":
        form = AddGroupForm(request.POST)
        if form.is_valid():
            if group.Exists(form.cleaned_data["common_name"]):
                return Error(request, "Alias already exists.")
            newGroup = group.Add(parent, str(form.cleaned_data["common_name"]))
            if not newGroup.parent == "None" and not newGroup.parent == "Besturen":
                newAction = newGroup.createGroupDir("ank.chnet")
                newAction.locked = False
            return HttpResponseRedirect("/groups/" + form.cleaned_data["common_name"])
    else:
        form = AddGroupForm()

    return render(request, "form.html", {"form": form, "uid": "groups"})


def rmGroup(request, cn):
    if request.method != "POST":
        raise Http404

    try:
        groupObj = group.FromCN(cn)
    except:
        raise Http404

    if len(action.GetAllActions({"affectedDN": groupObj.dn})) > 0:
        return Error(request, "Cannot remove group with pending actions.")

    groupObj.remove()
    return HttpResponseRedirect("/groups")
