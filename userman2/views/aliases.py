from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from userman2.forms.alias import *
from userman2.model.ldapconn import LDAPError
from userman2.views.error import Error


def displayAliases(request):
    if request.GET:
        form = AliasForm(request.GET)
        if form.is_valid():
            aliases = alias.getAllAliases(form.cleaned_data)
        else:
            aliases = alias.getAllAliases()
    else:
        form = AliasForm()
        aliases = alias.getAllAliases()

    return render(request, "groupsaliases.html", {"alias": True, "groups": aliases, "form": form})


def displayAlias(request, cn):
    try:
        aliasObj = alias.fromCN(cn)
    except:
        raise Http404
    return render(request, "groupalias.html", {"alias": True, "group": aliasObj})


def rmuser(request, cn, user):
    if request.method != "POST":
        raise Http404

    try:
        aliasObj = alias.fromCN(cn)
    except:
        raise Http404

    if not user in aliasObj.members:
        raise Http404

    aliasObj.connectRoot()
    aliasObj.removeMember(user)
    return HttpResponseRedirect("/aliases/" + aliasObj.cn)


def adduser(request, cn):
    try:
        aliasObj = alias.fromCN(cn)
    except Exception:
        raise Http404

    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            try:
                aliasObj.connectRoot()
                if form.cleaned_data["uid"]:
                    aliasObj.addMember(str(form.cleaned_data["uid"]))
                elif form.cleaned_data["alias"]:
                    aliasObj.addMember(str(form.cleaned_data["alias"]))
                elif form.cleaned_data["email"]:
                    aliasObj.addMember(str(form.cleaned_data["email"]))
                return HttpResponseRedirect("/aliases/" + aliasObj.cn)
            except LDAPError as e:
                return Error(request, e.message)
    else:
        form = AddUserForm()

    return render(request, "form.html", {"form": form, "uid": aliasObj.cn})


def addAlias(request, parent):
    if not parent in alias.GetParents():
        raise Http404

    if request.method == "POST":
        form = AddAliasForm(request.POST)
        if form.is_valid():
            if alias.Exists(form.cleaned_data["common_name"]):
                return Error(request, "Alias already exists.")
            if user.Exists(form.cleaned_data["common_name"]):
                return Error(request, "User with same name already exists.")
            alias.Add(parent, str(form.cleaned_data["common_name"]))
            return HttpResponseRedirect("/aliases/" + form.cleaned_data["common_name"])
    else:
        form = AddAliasForm()

    return render(request, "form.html", {"form": form, "uid": "aliases"})


def rmAlias(request, cn):
    if request.method != "POST":
        raise Http404

    try:
        aliasObj = alias.fromCN(cn)
    except:
        raise Http404

    aliasObj.connectRoot()
    aliasObj.remove()
    return HttpResponseRedirect("/aliases")
