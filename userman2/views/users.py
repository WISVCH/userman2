from datetime import datetime

import requests
from django.conf import settings
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_control

from userman2.forms.user import *
from userman2.model import action
from userman2.model import user


def getUsersJson(request):
    users = user.GetAllUsers()
    usersDict = [dict(name=u.uid, uid=u.uidNumber, full_name=u.gecos['full_name']) for u in users]
    return JsonResponse(usersDict, safe=False)


def getUserDienst2Status(request, uid):
    try:
        userObj = user.FromUID(uid)
    except:
        raise Http404
    dienst2Status = dienst2(uid)
    return JsonResponse(dienst2Status)


def displayUsers(request):
    return render(request, 'users.html')


def displayUser(request, uid):
    try:
        userObj = user.FromUID(uid)
    except:
        raise Http404
    dienst2Status = dienst2(uid)
    return render(request, 'user.html', {'user': userObj, 'dienst2Status': dienst2Status})


def userChfn(request, uid):
    try:
        userObj = user.FromUID(uid)
    except:
        raise Http404

    if request.method == 'POST':
        form = ChfnForm(request.POST)
        if form.is_valid():
            userObj.gecos = form.cleaned_data
            return HttpResponseRedirect('/users/' + userObj.uid)
    else:
        form = ChfnForm(initial=userObj.gecos)

    return render(request, 'form.html', {'form': form, 'uid': userObj.uid})


def userChdesc(request, uid):
    try:
        userObj = user.FromUID(uid)
    except:
        raise Http404

    if request.method == 'POST':
        form = ChdescForm(request.POST)
        if form.is_valid():
            userObj.description = str(form.cleaned_data["description"])
            return HttpResponseRedirect('/users/' + userObj.uid)
    else:
        form = ChdescForm(initial={"description": userObj.description})

    return render(request, 'form.html', {'form': form, 'uid': userObj.uid})


def userChwarnRm(request, uid):
    try:
        userObj = user.FromUID(uid)
    except:
        raise Http404

    if request.method == 'POST':
        form = ChwarnRmForm(request.POST)
        if form.is_valid():
            userObj.toBeDeleted = form.cleaned_data["toBeDeleted"]
            return HttpResponseRedirect('/users/' + userObj.uid)
    else:
        form = ChwarnRmForm(initial={"toBeDeleted": userObj.toBeDeleted})

    return render(request, 'form.html', {'form': form, 'uid': userObj.uid})


def userChsh(request, uid):
    try:
        userObj = user.FromUID(uid)
    except:
        raise Http404

    if request.method == 'POST':
        form = ChshForm(request.POST)
        if form.is_valid():
            userObj.loginShell = str(form.cleaned_data["login_shell"])
            return HttpResponseRedirect('/users/' + userObj.uid)
    else:
        form = ChshForm(initial={"login_shell": userObj.loginShell})

    return render(request, 'form.html', {'form': form, 'uid': userObj.uid})


def userChgroup(request, uid):
    try:
        userObj = user.FromUID(uid)
    except:
        raise Http404

    if request.method == 'POST':
        form = ChgroupForm(request.POST)
        if form.is_valid():
            userObj.gidNumber = str(form.cleaned_data["gid_number"])
            return HttpResponseRedirect('/users/' + userObj.uid)
    else:
        form = ChgroupForm(initial={"gid_number": userObj.gidNumber})

    return render(request, 'form.html', {'form': form, 'uid': userObj.uid})


def chHomeCH(request, uid):
    try:
        userObj = user.FromUID(uid)
    except:
        raise Http404

    if request.method == 'POST':
        form = ChHomeForm(request.POST)
        if form.is_valid():
            userObj.homeDirectoryCH = str(form.cleaned_data["new_directory"])
            return HttpResponseRedirect('/users/' + userObj.uid)
    else:
        form = ChHomeForm(initial={"new_directory": userObj.description})

    return render(request, 'form.html', {'form': form, 'uid': userObj.uid})


def chHomeAnk(request, uid):
    try:
        userObj = user.FromUID(uid)
    except:
        raise Http404

    if request.method == 'POST':
        form = ChHomeForm(request.POST)
        if form.is_valid():
            userObj.homeDirectoryAnk = str(form.cleaned_data["new_directory"])
            return HttpResponseRedirect('/users/' + userObj.uid)
    else:
        form = ChHomeForm(initial={"new_directory": userObj.description})

    return render(request, 'form.html', {'form': form, 'uid': userObj.uid})


def userChpriv(request, uid):
    try:
        userObj = user.FromUID(uid)
    except:
        raise Http404

    if request.method == 'POST':
        form = ChprivForm(request.POST)
        if form.is_valid():
            serviceStr = str(form.cleaned_data["service"])
            if serviceStr not in userObj.authorizedServices:
                userObj.addAuthorizedService(serviceStr)
                return HttpResponseRedirect('/users/' + userObj.uid + '/chpriv')
    else:
        form = ChprivForm()

    return render(request, 'userpriv.html', {'form': form, 'user': userObj})


def userRmpriv(request, uid, service, server):
    if request.method != 'POST':
        raise Http404

    try:
        userObj = user.FromUID(uid)
    except:
        raise Http404
    serviceStr = service + "@" + server
    if not serviceStr in userObj.authorizedServices:
        raise Http404
    userObj.removeAuthorizedService(serviceStr)
    return HttpResponseRedirect('/users/' + userObj.uid + '/chpriv')


def userShowldif(request, uid):
    try:
        userObj = user.FromUID(uid)
    except Exception as e:
        raise Http404

    print(userObj.ldif)

    return render(request, 'usershowldif.html', {'user': userObj})


def addUser(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            if user.Exists(form.cleaned_data['uid']):
                raise Http404
            newUser = user.Add(str(form.cleaned_data['uid']), str(
                form.cleaned_data['full_name']))

            for access in form.cleaned_data['access']:
                newUser.addAuthorizedService(str(access))
            # newUser.createSambaEntry()

            return HttpResponseRedirect('/users/' + form.cleaned_data['uid'])
    else:
        form = AddUserForm()

    return render(request, 'form.html', {'form': form, 'uid': "users"})


def rmUser(request, uid):
    if request.method != 'POST':
        raise Http404

    try:
        userObj = user.FromUID(uid)
    except Exception as e:
        raise Http404

    userObj.remove()
    return HttpResponseRedirect('/users')


def removeProfile(request, uid):
    if request.method != 'POST':
        raise Http404

    try:
        userObj = user.FromUID(uid)
    except Exception as e:
        raise Http404

    newAction = userObj.removeProfile('ank.chnet')
    newAction.locked = False
    return HttpResponseRedirect('/users/' + userObj.uid)


def resetPassword(request, uid):
    if request.method != 'POST':
        raise Http404

    try:
        userObj = user.FromUID(uid)
    except Exception as e:
        raise Http404

    dienst2Status = dienst2(uid)
    password = userObj.resetPassword()
    return render(request, 'user.html', {'user': userObj, 'dienst2Status': dienst2Status, 'password': password})


def chPassword(request, uid):
    try:
        userObj = user.FromUID(uid)
    except Exception as e:
        raise Http404

    if request.method == 'POST':
        form = ChpassForm(request.POST)
        if form.is_valid():
            userObj.changePassword(form.cleaned_data['password'])
            return HttpResponseRedirect('/users/' + userObj.uid)
    else:
        form = ChpassForm()

    return render(request, 'form.html', {'form': form, 'user': userObj})


def dienst2(username):
    if username in settings.DIENST2_WHITELIST:
        return {'status': 'whitelisted', 'message': 'Whitelisted'}

    headers = {'Authorization': 'Token ' + settings.DIENST2_APITOKEN}
    url = settings.DIENST2_BASEURL + '/ldb/api/v3/people/'
    link_prefix = 'https://dienst2.chnet/ldb/people/%d/'
    try:
        r = requests.get(url, params={'ldap_username': username}, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
    if r.status_code is not 200:
        return {'error': "Status code %d" % r.status_code}

    json = r.json()
    n = len(json['results'])
    if n is 0:
        ret = {'status': 'error', 'message': 'Username not found in Dienst2'}
    elif n > 1:
        ret = {'status': 'error', 'message': 'Error: %d records matched' % n}
    else:
        if json['results'][0]['membership_status'] >= 30:
            ret = {'status': 'success', 'message': 'Active member'}
        else:
            ret = {'status': 'warning', 'message': 'Not an active member'}
        ret['id'] = json['results'][0]['id']
        ret['href'] = link_prefix % json['results'][0]['id']
    return ret
