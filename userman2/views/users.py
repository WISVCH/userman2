from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from userman2.dienst2 import fetchDienst2Status, usernameInDienst2
from userman2.forms.user import *
from userman2.model import action, alias
from userman2.model import user
from userman2.views.error import Error


def getUsersJson(request):
    users = user.GetAllUsers()
    usersDict = [dict(name=u.uid, uid=u.uidNumber, full_name=u.gecos["full_name"]) for u in users]
    return JsonResponse(usersDict, safe=False)


def getUserDienst2Status(request, uid):
    if not user.Exists(uid):
        raise Http404
    dienst2Status = fetchDienst2Status(uid)
    return JsonResponse(dienst2Status)


def displayUsers(request):
    return render(request, "users.html")


def displayUser(request, uid):
    try:
        userObj = user.FromUID(uid)
    except:
        raise Http404
    return render(request, "user.html", {"user": userObj})


def userChfn(request, uid):
    try:
        userObj = user.FromUID(uid)
    except:
        raise Http404

    if request.method == "POST":
        form = ChfnForm(request.POST)
        if form.is_valid():
            userObj.gecos = form.cleaned_data
            return HttpResponseRedirect("/users/" + userObj.uid)
    else:
        form = ChfnForm(initial=userObj.gecos)

    return render(request, "form.html", {"form": form, "uid": userObj.uid})


def userChdesc(request, uid):
    try:
        userObj = user.FromUID(uid)
    except:
        raise Http404

    if request.method == "POST":
        form = ChdescForm(request.POST)
        if form.is_valid():
            userObj.description = str(form.cleaned_data["description"])
            return HttpResponseRedirect("/users/" + userObj.uid)
    else:
        form = ChdescForm(initial={"description": userObj.description})

    return render(request, "form.html", {"form": form, "uid": userObj.uid})


def userChsh(request, uid):
    try:
        userObj = user.FromUID(uid)
    except:
        raise Http404

    if request.method == "POST":
        form = ChshForm(request.POST)
        if form.is_valid():
            userObj.loginShell = str(form.cleaned_data["login_shell"])
            return HttpResponseRedirect("/users/" + userObj.uid)
    else:
        form = ChshForm(initial={"login_shell": userObj.loginShell})

    return render(request, "form.html", {"form": form, "uid": userObj.uid})


def userChgroup(request, uid):
    try:
        userObj = user.FromUID(uid)
    except:
        raise Http404

    if request.method == "POST":
        form = ChgroupForm(request.POST)
        if form.is_valid():
            userObj.gidNumber = str(form.cleaned_data["gid_number"])
            return HttpResponseRedirect("/users/" + userObj.uid)
    else:
        form = ChgroupForm(initial={"gid_number": userObj.gidNumber})

    return render(request, "form.html", {"form": form, "uid": userObj.uid})


def userChpriv(request, uid):
    try:
        userObj = user.FromUID(uid)
    except:
        raise Http404

    if request.method == "POST":
        form = ChprivForm(request.POST)
        if form.is_valid():
            serviceStr = str(form.cleaned_data["service"])
            if serviceStr not in userObj.authorizedServices:
                userObj.addAuthorizedService(serviceStr)
                return HttpResponseRedirect("/users/" + userObj.uid + "/chpriv")
    else:
        form = ChprivForm()

    return render(request, "userpriv.html", {"form": form, "user": userObj})


def userRmpriv(request, uid, service, server):
    if request.method != "POST":
        raise Http404

    try:
        userObj = user.FromUID(uid)
    except:
        raise Http404
    serviceStr = service + "@" + server
    if not serviceStr in userObj.authorizedServices:
        raise Http404
    userObj.removeAuthorizedService(serviceStr)
    return HttpResponseRedirect("/users/" + userObj.uid + "/chpriv")


def addUser(request):
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            uid = form.cleaned_data["uid"]
            if user.Exists(uid):
                return Error(request, "User already exists.")
            if alias.Exists(uid):
                return Error(request, "Alias with same name already exists.")
            if usernameInDienst2(uid):
                return Error(request, "Username already exists in Dienst2.")
            newUser = user.Add(str(uid), str(form.cleaned_data["full_name"]))

            for access in form.cleaned_data["access"]:
                newUser.addAuthorizedService(str(access))

            return HttpResponseRedirect("/users/" + uid)
    else:
        form = AddUserForm()

    return render(request, "form.html", {"form": form, "uid": "users"})


def rmUser(request, uid):
    if request.method != "POST":
        raise Http404

    try:
        userObj = user.FromUID(uid)
    except Exception as e:
        raise Http404

    if len(action.GetAllActions({"affectedDN": userObj.dn})) > 0:
        return Error(request, "Cannot remove user with pending actions.")

    userObj.remove()
    return HttpResponseRedirect("/actions")


def resetPassword(request, uid):
    if request.method != "POST":
        raise Http404

    try:
        userObj = user.FromUID(uid)
    except Exception as e:
        raise Http404

    password = userObj.resetPassword()
    return JsonResponse({"password": password})
