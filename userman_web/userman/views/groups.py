from userman.model import group
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.cache import cache_control

from userman.forms.group import *

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
    
    return render_to_response('groups.html', {'groups': groups, 'form': form})


@cache_control(no_cache=True, must_revalidate=True)
def displayGroup(request, cn):
    try:
	groupObj = group.fromCN(cn)
    except Exception, e:
	raise Http404
    return render_to_response('group.html', {'group': groupObj})
	 
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
