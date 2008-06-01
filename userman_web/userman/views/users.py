from userman.model import user
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.cache import cache_control

from userman.forms.user import *

def displayUsers(request):
    if (request.GET):
	form = UsersForm(request.GET)
	if form.is_valid():
	    users = user.getAllUsers(form.clean_data)
	else:
    	    users = user.getAllUsers()
    else:
	form = UsersForm()
	users = user.getAllUsers()
    
    return render_to_response('users.html', {'users': users, 'form': form})


@cache_control(no_cache=True, must_revalidate=True)
def displayUser(request, uid):
    try:
	userObj = user.fromUID(uid)
    except Exception, e:
	raise Http404
    return render_to_response('user.html', {'user': userObj})
	 

@cache_control(no_cache=True, must_revalidate=True)
def userChfn(request, uid):
    try:
        userObj = user.fromUID(uid)
    except Exception, e:
        raise Http404
    
    if request.method == 'POST':
	form = ChfnForm(request.POST)
	if form.is_valid():
	    userObj.gecos = form.clean_data
	    return HttpResponseRedirect('/users/' + userObj.uid +'/')
    else:
	    form = ChfnForm( initial=userObj.gecos)
    				    
    return render_to_response('form.html', {'form': form, 'uid': userObj.uid})

@cache_control(no_cache=True, must_revalidate=True)
def userChdesc(request, uid):
    try:
        userObj = user.fromUID(uid)
    except Exception, e:
        raise Http404
    
    if request.method == 'POST':
	form = ChdescForm(request.POST)
	if form.is_valid():
	    userObj.description = form.clean_data["description"]
	    return HttpResponseRedirect('/users/' + userObj.uid +'/')
    else:
	    form = ChdescForm( initial={"description": userObj.description})
    				    
    return render_to_response('form.html', {'form': form, 'uid': userObj.uid})

@cache_control(no_cache=True, must_revalidate=True)
def userChsh(request, uid):
    try:
        userObj = user.fromUID(uid)
    except Exception, e:
        raise Http404
    
    if request.method == 'POST':
	form = ChshForm(request.POST)
	if form.is_valid():
	    userObj.loginShell = str(form.clean_data["login_shell"])
	    return HttpResponseRedirect('/users/' + userObj.uid +'/')
    else:
	    form = ChshForm( initial={"login_shell": userObj.loginShell})

    return render_to_response('form.html', {'form': form, 'uid': userObj.uid})


@cache_control(no_cache=True, must_revalidate=True)
def userChgroup(request, uid):
    try:
        userObj = user.fromUID(uid)
    except Exception, e:
        raise Http404
    
    if request.method == 'POST':
	form = ChgroupForm(request.POST)
	if form.is_valid():
	    userObj.gidNumber = str(form.clean_data["gid_number"])
	    return HttpResponseRedirect('/users/' + userObj.uid +'/')
    else:
	    form = ChgroupForm( initial={"gid_number": userObj.gidNumber})

    return render_to_response('form.html', {'form': form, 'uid': userObj.uid})

@cache_control(no_cache=True, must_revalidate=True)
def userChpriv(request, uid):
    try:
        userObj = user.fromUID(uid)
    except Exception, e:
        raise Http404
    
    if request.method == 'POST':
	form = ChprivForm(request.POST)
	if form.is_valid():
	    serviceStr = str(form.clean_data["service"]) + "@" + str(form.clean_data["server"])
	    if not serviceStr in userObj.authorizedServices:
		userObj.addAuthorizedService(str(form.clean_data["service"]) + "@" + str(form.clean_data["server"]))
		return HttpResponseRedirect('/users/' + userObj.uid +'/chpriv/')
    else:
	    form = ChprivForm()

    return render_to_response('userpriv.html', {'form': form, 'user': userObj})

def userRmpriv(request, uid, service, server):
    try:
        userObj = user.fromUID(uid)
    except Exception, e:
        raise Http404
    serviceStr = service + "@" + server
    if not serviceStr in userObj.authorizedServices:
        raise Http404
    userObj.removeAuthorizedService(serviceStr)
    return HttpResponseRedirect('/users/' + userObj.uid +'/chpriv/')

@cache_control(no_cache=True, must_revalidate=True)
def userShowldif(request, uid):
    try:
        userObj = user.fromUID(uid)
    except Exception, e:
        raise Http404

    print userObj.ldif

    return render_to_response('usershowldif.html', {'user': userObj})
