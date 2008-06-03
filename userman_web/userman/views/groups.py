from userman.model import group
from userman.model import action

from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.cache import cache_control

from userman.forms.group import *

@cache_control(no_cache=True, must_revalidate=True)
def displayGroups(request):
    if (request.GET):
        form = GroupsForm(request.GET)
        if form.is_valid():
            groups = group.GetAllGroups(form.clean_data)
        else:
            groups = group.GetAllGroups()
    else:
        form = GroupsForm()
        groups = group.GetAllGroups()
    
    return render_to_response('groupsaliases.html', {'groups': groups, 'form': form})


@cache_control(no_cache=True, must_revalidate=True)
def displayGroup(request, cn):
    try:
        groupObj = group.FromCN(cn)
    except Exception, e:
        raise Http404
    return render_to_response('groupalias.html', {'group': groupObj})

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
            groupObj.addMember(str(form.clean_data["user"]))
            return HttpResponseRedirect('/groups/' + groupObj.cn + '/')
    else:
        form = AddUserForm()

    return render_to_response('form.html', {'form': form, 'uid': groupObj.cn})

def addGroup(request, parent):
    if not parent in group.GetParents():
        raise Http404
    
    if request.method == 'POST':
        form = AddGroupForm(request.POST)
        if form.is_valid():
            if group.Exists(form.clean_data['common_name']):
                raise Http404
            newGroup = group.Add(parent, str(form.clean_data['common_name']))
            if not newGroup.parent == "None" and not newGroup.parent == "Besturen":
                newAction = newGroup.createGroupDir('ank.chnet')
                newAction.locked = False

# TODO            newGroup.addGroupMapping()
            return HttpResponseRedirect('/groups/' + form.clean_data['common_name'] + '/')
    else:
        form = AddGroupForm()
    
    return render_to_response('form.html', {'form': form, 'uid': "groups"})

def rmGroup(request, cn):
    try:
        groupObj = group.FromCN(cn)
    except Exception, e:
        raise Http404
    
    groupObj.remove()
    
    return HttpResponseRedirect('/groups/')
 