from random import randint
from datetime import datetime

from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.cache import cache_control
from django.conf import settings
import requests

from django.core.cache import cache

from settings import DIENST2_WHITELIST, DIENST2_APIKEY
from userman2.model import user
from userman2.model import action
from userman2.forms.user import *


@cache_control(no_cache=True, must_revalidate=True)
def displayUsers(request):
    if (request.GET):
        form = UsersForm(request.GET)
        if form.is_valid():
            users = user.GetAllUsers(form.cleaned_data)
        else:
            users = user.GetAllUsers()
    else:
        form = UsersForm()
        users = user.GetAllUsers()

    rmWarnUsers = [user.User(curaction.affectedDN)
                   .uid for curaction in action.GetAllActions({"actionName": "warnRemove"})]

    session = requests.Session()

    count = {"total": 0, "del": 0, "chlocal": 0, "anklocal": 0, "anksamba": 0}
    for u in users:
            count["total"] += 1
            # Disabled because it will make an LDAP request for every user
            # if u.toBeDeleted:
            #    count["del"] += 1
            if u.chLocal:
                count["chlocal"] += 1
            if u.ankLocal:
                count["anklocal"] += 1
            if u.ankSamba:
                count["anksamba"] += 1
            u.dienst2Status = dienst2_cached(u.uid, session)

    return render_to_response('users.html', {'users': users, 'form': form, 'count': count, 'rmWarnUsers': rmWarnUsers})


@cache_control(no_cache=True, must_revalidate=True)
def displayUser(request, uid):
    try:
        userObj = user.FromUID(uid)
    except Exception, e:
        raise Http404
    dienst2Status = dienst2(uid, requests.session())
    return render_to_response('user.html', {'user': userObj, 'dienst2Status': dienst2Status})


@cache_control(no_cache=True, must_revalidate=True)
def userChfn(request, uid):
    try:
        userObj = user.FromUID(uid)
    except Exception, e:
        raise Http404

    if request.method == 'POST':
        form = ChfnForm(request.POST)
        if form.is_valid():
            userObj.gecos = form.cleaned_data
            return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid + '/')
    else:
            form = ChfnForm(initial=userObj.gecos)

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
            userObj.description = str(form.cleaned_data["description"])
            return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid + '/')
    else:
            form = ChdescForm(initial={"description": userObj.description})

    return render_to_response('form.html', {'form': form, 'uid': userObj.uid})


@cache_control(no_cache=True, must_revalidate=True)
def userChwarnRm(request, uid):
    try:
        userObj = user.FromUID(uid)
    except Exception, e:
        raise Http404

    if request.method == 'POST':
        form = ChwarnRmForm(request.POST)
        if form.is_valid():
            userObj.toBeDeleted = form.cleaned_data["toBeDeleted"]
            return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid + '/')
    else:
            form = ChwarnRmForm(initial={"toBeDeleted": userObj.toBeDeleted})

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
            userObj.loginShell = str(form.cleaned_data["login_shell"])
            return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid + '/')
    else:
            form = ChshForm(initial={"login_shell": userObj.loginShell})

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
            userObj.gidNumber = str(form.cleaned_data["gid_number"])
            return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid + '/')
    else:
            form = ChgroupForm(initial={"gid_number": userObj.gidNumber})

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
            userObj.homeDirectoryCH = str(form.cleaned_data["new_directory"])
            return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid + '/')
    else:
        form = ChHomeForm(initial={"new_directory": userObj.description})

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
            userObj.homeDirectoryAnk = str(form.cleaned_data["new_directory"])
            return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid + '/')
    else:
        form = ChHomeForm(initial={"new_directory": userObj.description})

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
            serviceStr = str(form.cleaned_data["service"]) + "@" + str(
                form.cleaned_data["server"])
            if not serviceStr in userObj.authorizedServices:
                userObj.addAuthorizedService(str(
                    form.cleaned_data["service"]) + "@" + str(form.cleaned_data["server"]))
                return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid + '/chpriv/')
    else:
            form = ChprivForm()

    return render_to_response('userpriv.html', {'form': form, 'user': userObj})


@cache_control(no_cache=True, must_revalidate=True)
def userRmpriv(request, uid, service, server):
    try:
        userObj = user.FromUID(uid)
    except Exception, e:
        raise Http404
    serviceStr = service + "@" + server
    if not serviceStr in userObj.authorizedServices:
        raise Http404
    userObj.removeAuthorizedService(serviceStr)
    return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid + '/chpriv/')


@cache_control(no_cache=True, must_revalidate=True)
def userShowldif(request, uid):
    try:
        userObj = user.FromUID(uid)
    except Exception, e:
        raise Http404

    print userObj.ldif

    return render_to_response('usershowldif.html', {'user': userObj})


@cache_control(no_cache=True, must_revalidate=True)
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
#            newUser.createSambaEntry()

            return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + form.cleaned_data['uid'] + '/')
    else:
        form = AddUserForm()

    return render_to_response('form.html', {'form': form, 'uid': "users"})


@cache_control(no_cache=True, must_revalidate=True)
def rmUser(request, uid):
    try:
        userObj = user.FromUID(uid)
    except Exception, e:
        raise Http404

    userObj.remove()
    return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/')


@cache_control(no_cache=True, must_revalidate=True)
def removeProfile(request, uid):
    try:
        userObj = user.FromUID(uid)
    except Exception, e:
        raise Http404

    newAction = userObj.removeProfile('ank.chnet')
    newAction.locked = False
    return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid + '/')


@cache_control(no_cache=True, must_revalidate=True)
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
            userObj.changePassword(form.cleaned_data['password'])
            return HttpResponseRedirect(settings.USERMAN_PREFIX + '/users/' + userObj.uid + '/')
    else:
        form = ChpassForm()

    return render_to_response('form.html', {'form': form, 'user': userObj})


def dienst2(username, session):
    if username in DIENST2_WHITELIST:
        return {'status': 'whitelisted', 'message': 'Whitelisted'}

    headers = {'Authorization': 'ApiKey ' + DIENST2_APIKEY}
    url = 'https://frans.chnet/dienst2/ldb/api/v2/person/'
    link_prefix = 'https://frans.chnet/dienst2/ldb/#/person/%d'
    try:
        r = session.get(url, params={'ldap_username': username}, headers=headers)
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
    if r.status_code is not 200:
        return {'error': "Status code %d" % r.status_code}

    json = r.json()
    n = len(json['objects'])
    if n is 0:
        ret = {'status': 'warning', 'message': 'Not found'}
    elif n > 1:
        ret = {'status': 'error', 'message': 'Error: %d records matched' % n}
    else:
        ret = {'status': 'success', 'message': 'Found one matching record', 'href': link_prefix % json['objects'][0]['id']}

    ret['updated'] = str(datetime.now())
    cache.set('dienst2status_' + username, ret, randint(3600, 86400))
    return ret


def dienst2_cached(username, session):
    ret = cache.get('dienst2status_' + username)
    if ret is None:
        ret = dienst2(username, session)
    return ret
