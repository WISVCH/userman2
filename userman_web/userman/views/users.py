from userman.model import user
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.cache import cache_control
from django.conf import settings

from userman.forms.user import *

def displayUsers(request):
    if (request.GET):
	form = UsersForm(request.GET)
	if form.is_valid():
	    users = user.GetAllUsers(form.clean_data)
	else:
    	    users = user.GetAllUsers()
    else:
	form = UsersForm()
	users = user.GetAllUsers()

    count = {"total":0, "del":0, "chlocal":0, "chsamba":0, "anklocal":0, "anksamba":0}
    for u in users:
            count["total"] += 1
            # FIXME: Moet nog geimplementeerd worden
            #if u.toBeDeleted:
            #	count["del"] += 1
            if u.chLocal:
                    count["chlocal"] += 1
            if u.chSamba:
                    count["chsamba"] += 1
            if u.ankLocal:
                    count["anklocal"] += 1
            if u.ankSamba:
                    count["anksamba"] += 1
    
    return render_to_response('users.html', {'users': users, 'form': form, 'count': count})


@cache_control(no_cache=True, must_revalidate=True)
def displayUser(request, uid):
    try:
	userObj = user.FromUID(uid)
    except Exception, e:
	raise Http404
    return render_to_response('user.html', {'user': userObj})
	 

@cache_control(no_cache=True, must_revalidate=True)
def userChfn(request, uid):
    try:
        userObj = user.FromUID(uid)
    except Exception, e:
        raise Http404
    
    if request.method == 'POST':
	form = ChfnForm(request.POST)
	if form.is_valid():
	    userObj.gecos = form.clean_data
	    return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid +'/')
    else:
	    form = ChfnForm( initial=userObj.gecos)
    				    
    return render_to_response('form.html', {'form': form, 'uid': userObj.uid})

@cache_control(no_cache=True, must_revalidate=True)
def userChdesc(request, uid):
    try:
        userObj = user.FromUID(uid)
    except Exception, e:
        raise Http404
    
    if request.method == 'POST':
	form = ChdescForm(request.POST)
	if form.is_valid():
	    userObj.description = str(form.clean_data["description"])
	    return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid +'/')
    else:
	    form = ChdescForm( initial={"description": userObj.description})
    				    
    return render_to_response('form.html', {'form': form, 'uid': userObj.uid})

@cache_control(no_cache=True, must_revalidate=True)
def userChsh(request, uid):
    try:
        userObj = user.FromUID(uid)
    except Exception, e:
        raise Http404
    
    if request.method == 'POST':
	form = ChshForm(request.POST)
	if form.is_valid():
	    userObj.loginShell = str(form.clean_data["login_shell"])
	    return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid +'/')
    else:
	    form = ChshForm( initial={"login_shell": userObj.loginShell})

    return render_to_response('form.html', {'form': form, 'uid': userObj.uid})


@cache_control(no_cache=True, must_revalidate=True)
def userChgroup(request, uid):
    try:
        userObj = user.FromUID(uid)
    except Exception, e:
        raise Http404
    
    if request.method == 'POST':
	form = ChgroupForm(request.POST)
	if form.is_valid():
	    userObj.gidNumber = str(form.clean_data["gid_number"])
	    return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid +'/')
    else:
	    form = ChgroupForm( initial={"gid_number": userObj.gidNumber})

    return render_to_response('form.html', {'form': form, 'uid': userObj.uid})

@cache_control(no_cache=True, must_revalidate=True)
def chHomeCH(request, uid):
    try:
        userObj = user.FromUID(uid)
    except Exception, e:
        raise Http404
    
    if request.method == 'POST':
        form = ChHomeForm(request.POST)
        if form.is_valid():
            userObj.homeDirectoryCH = str(form.clean_data["new_directory"])
            return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid +'/')
    else:
        form = ChHomeForm( initial={"new_directory": userObj.description})
                        
    return render_to_response('form.html', {'form': form, 'uid': userObj.uid})

@cache_control(no_cache=True, must_revalidate=True)
def chHomeAnk(request, uid):
    try:
        userObj = user.FromUID(uid)
    except Exception, e:
        raise Http404
    
    if request.method == 'POST':
        form = ChHomeForm(request.POST)
        if form.is_valid():
            userObj.homeDirectoryAnk = str(form.clean_data["new_directory"])
            return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid +'/')
    else:
        form = ChHomeForm( initial={"new_directory": userObj.description})
                        
    return render_to_response('form.html', {'form': form, 'uid': userObj.uid})

@cache_control(no_cache=True, must_revalidate=True)
def userChpriv(request, uid):
    try:
        userObj = user.FromUID(uid)
    except Exception, e:
        raise Http404
    
    if request.method == 'POST':
	form = ChprivForm(request.POST)
	if form.is_valid():
	    serviceStr = str(form.clean_data["service"]) + "@" + str(form.clean_data["server"])
	    if not serviceStr in userObj.authorizedServices:
		userObj.addAuthorizedService(str(form.clean_data["service"]) + "@" + str(form.clean_data["server"]))
		return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid +'/chpriv/')
    else:
	    form = ChprivForm()

    return render_to_response('userpriv.html', {'form': form, 'user': userObj})

def userRmpriv(request, uid, service, server):
    try:
        userObj = user.FromUID(uid)
    except Exception, e:
        raise Http404
    serviceStr = service + "@" + server
    if not serviceStr in userObj.authorizedServices:
        raise Http404
    userObj.removeAuthorizedService(serviceStr)
    return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid +'/chpriv/')

@cache_control(no_cache=True, must_revalidate=True)
def userShowldif(request, uid):
    try:
        userObj = user.FromUID(uid)
    except Exception, e:
        raise Http404

    print userObj.ldif

    return render_to_response('usershowldif.html', {'user': userObj})

def addUser(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            if user.Exists(form.clean_data['uid']):
                raise Http404
            newUser = user.Add(str(form.clean_data['uid']), str(form.clean_data['full_name']))
            newUser.createHomeDir('ank.chnet').locked = False
            newUser.createHomeDir('ch.chnet').locked = False
            newUser.createMailbox('ch.chnet').locked = False
            newUser.generateLogonScript('ank.chnet').locked = False
            for access in form.clean_data['access']:
                newUser.addAuthorizedService(str(access))
#            newUser.createSambaEntry()
            
            return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + form.clean_data['uid'] + '/')
    else:
        form = AddUserForm()
    
    return render_to_response('form.html', {'form': form, 'uid': "users"})

def rmUser(request, uid):
    try:
        userObj = user.FromUID(uid)    
    except Exception, e:
        raise Http404
    
    userObj.remove()
    return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/')

def removeProfile(request, uid):
    try:
        userObj = user.FromUID(uid)    
    except Exception, e:
        raise Http404
    
    newAction = userObj.removeProfile('ank.chnet')
    newAction.locked = False
    return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid + '/')

def genLoginScript(request, uid):
    try:
        userObj = user.FromUID(uid)    
    except Exception, e:
        raise Http404
    
    newAction = userObj.generateLogonScript('ank.chnet')
    newAction.locked = False
    return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid + '/')

def resetPassword(request, uid):
    try:
        userObj = user.FromUID(uid)    
    except Exception, e:
        raise Http404
    
    userObj.resetPassword()
    return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid + '/')

@cache_control(no_cache=True, must_revalidate=True)
def chPassword(request, uid):
    try:
        userObj = user.FromUID(uid)
    except Exception, e:
        raise Http404
    
    if request.method == 'POST':
        form = ChpassForm(request.POST)
        if form.is_valid():
            userObj.changePassword(form.clean_data['password'])
            return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid +'/')
    else:
        form = ChpassForm()

    return render_to_response('form.html', {'form': form, 'user': userObj})
