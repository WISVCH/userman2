from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.cache import cache_control

from userman2.forms.group import *
from userman2.model import group


@cache_control(no_cache=True, must_revalidate=True)
def displayGroups(request):
    if (request.GET):
        form = GroupsForm(request.GET)
        if form.is_valid():
            groups = group.GetAllGroups(form.cleaned_data)
        else:
            groups = group.GetAllGroups()
    else:
        form = GroupsForm()
        groups = group.GetAllGroups()

    return render(request, 'groupsaliases.html', {'groups': groups, 'form': form})


@cache_control(no_cache=True, must_revalidate=True)
def displayGroup(request, cn):
    try:
        groupObj = group.FromCN(cn)
    except Exception, e:
        raise Http404
    return render(request, 'groupalias.html', {'group': groupObj})


@cache_control(no_cache=True, must_revalidate=True)
def rmuser(request, cn, user):
    try:
        groupObj = group.FromCN(cn)
    except Exception, e:
        raise Http404

    if not user in groupObj.members:
        raise Http404

    groupObj.connectRoot()
    groupObj.removeMember(user)
    return HttpResponseRedirect('/groups/' + groupObj.cn + '/')


@cache_control(no_cache=True, must_revalidate=True)
def adduser(request, cn):
    try:
        groupObj = group.FromCN(cn)
    except Exception, e:
        raise Http404

    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            groupObj.connectRoot()
            groupObj.addMember(str(form.cleaned_data["user"]))
            return HttpResponseRedirect('/groups/' + groupObj.cn + '/')
    else:
        form = AddUserForm()

    return render(request, 'form.html', {'form': form, 'uid': groupObj.cn})


@cache_control(no_cache=True, must_revalidate=True)
def addGroup(request, parent):
    if not parent in group.GetParents():
        raise Http404

    if request.method == 'POST':
        form = AddGroupForm(request.POST)
        if form.is_valid():
            if group.Exists(form.cleaned_data['common_name']):
                raise Http404
            newGroup = group.Add(parent, str(form.cleaned_data['common_name']))
            if not newGroup.parent == "None" and not newGroup.parent == "Besturen":
                newAction = newGroup.createGroupDir('ank.chnet')
                newAction.locked = False
            return HttpResponseRedirect('/groups/' + form.cleaned_data['common_name'] + '/')
    else:
        form = AddGroupForm()

    return render(request, 'form.html', {'form': form, 'uid': "groups"})


@cache_control(no_cache=True, must_revalidate=True)
def rmGroup(request, cn):
    try:
        groupObj = group.FromCN(cn)
    except Exception, e:
        raise Http404

    groupObj.remove()

    return HttpResponseRedirect('/groups/')
