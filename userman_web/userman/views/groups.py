from userman.model import group
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.cache import cache_control

from userman.forms.group import *

@cache_control(no_cache=True, must_revalidate=True)
def displayGroups(request):
    if (request.GET):
        form = GroupsForm(request.GET)
        if form.is_valid():
            groups = group.getAllGroups(form.clean_data)
        else:
            groups = group.getAllGroups()
    else:
        form = GroupsForm()
        groups = group.getAllGroups()
    
    return render_to_response('groupsaliases.html', {'groups': groups, 'form': form})


@cache_control(no_cache=True, must_revalidate=True)
def displayGroup(request, cn):
    try:
        groupObj = group.fromCN(cn)
    except Exception, e:
        raise Http404
    return render_to_response('groupalias.html', {'group': groupObj})

@cache_control(no_cache=True, must_revalidate=True)
def rmuser(request, cn, user):
    try:
        groupObj = group.fromCN(cn)
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
        groupObj = group.fromCN(cn)
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


#@cache_control(no_cache=True, must_revalidate=True)
#def groupChfn(request, uid):
#    try:
#        userObj = user.fromUID(uid)
#    except Exception, e:
#        raise Http404
#    
#    if request.method == 'POST':
#	form = ChfnForm(request.POST)
#	if form.is_valid():
#	    userObj.gecos = form.clean_data
#	    return HttpResponseRedirect('/users/' + userObj.uid +'/')
#    else:
#	    form = ChfnForm( initial=userObj.gecos)
#    				    
#    return render_to_response('form.html', {'form': form, 'uid': userObj.uid})

#@cache_control(no_cache=True, must_revalidate=True)
#def userChdesc(request, uid):
#    try:
#        userObj = user.fromUID(uid)
#    except Exception, e:
#        raise Http404
    
#    if request.method == 'POST':
#	form = ChdescForm(request.POST)
#	if form.is_valid():
#	    userObj.description = form.clean_data["description"]
#	    return HttpResponseRedirect('/users/' + userObj.uid +'/')
#    else:
#	    form = ChdescForm( initial={"description": userObj.description})
#    				    
#    return render_to_response('form.html', {'form': form, 'uid': userObj.uid})
#
