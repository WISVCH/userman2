from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_control

from userman2.forms.alias import *
from userman2.model.ldapconn import LDAPError


@cache_control(no_cache=True, must_revalidate=True)
def displayAliases(request):
    if (request.GET):
        form = AliasForm(request.GET)
        if form.is_valid():
            aliases = alias.getAllAliases(form.cleaned_data)
        else:
            aliases = alias.getAllAliases()
    else:
        form = AliasForm()
        aliases = alias.getAllAliases()

    return render_to_response('groupsaliases.html', {'alias': True, 'groups': aliases, 'form': form})


@cache_control(no_cache=True, must_revalidate=True)
def displayAlias(request, cn):
    try:
        aliasObj = alias.fromCN(cn)
    except Exception, e:
        raise Http404
    return render_to_response('groupalias.html', {'group': aliasObj})


@cache_control(no_cache=True, must_revalidate=True)
def rmuser(request, cn, user):
    try:
        aliasObj = alias.fromCN(cn)
    except Exception, e:
        raise Http404

    if not user in aliasObj.members:
        raise Http404

    aliasObj.connectRoot()
    aliasObj.removeMember(user)
    return HttpResponseRedirect('/aliases/' + aliasObj.cn + '/')


@cache_control(no_cache=True, must_revalidate=True)
def adduser(request, cn):
    try:
        aliasObj = alias.fromCN(cn)
    except Exception:
        raise Http404

    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            try:
                aliasObj.connectRoot()
                if form.cleaned_data['uid']:
                    aliasObj.addMember(str(form.cleaned_data['uid']))
                elif form.cleaned_data['alias']:
                    aliasObj.addMember(str(form.cleaned_data['alias']))
                elif form.cleaned_data['email']:
                    aliasObj.addMember(str(form.cleaned_data['email']))
                return HttpResponseRedirect('/aliases/' + aliasObj.cn + '/')
            except LDAPError as e:
                return render_to_response('error.html', {'msg': e.message})
    else:
        form = AddUserForm()

    return render_to_response('form.html', {'form': form, 'uid': aliasObj.cn})


@cache_control(no_cache=True, must_revalidate=True)
def addAlias(request, parent):
    if not parent in alias.GetParents():
        raise Http404

    if request.method == 'POST':
        form = AddAliasForm(request.POST)
        if form.is_valid():
            if alias.Exists(form.cleaned_data['common_name']):
                raise Http404
            alias.Add(parent, str(form.cleaned_data['common_name']))
            return HttpResponseRedirect('/aliases/' + form.cleaned_data['common_name'] + '/')
    else:
        form = AddAliasForm()

    return render_to_response('form.html', {'form': form, 'uid': "aliases"})


@cache_control(no_cache=True, must_revalidate=True)
def rmAlias(request, cn):
    try:
        aliasObj = alias.fromCN(cn)
    except Exception, e:
        raise Http404

    aliasObj.connectRoot()
    aliasObj.remove()
    return HttpResponseRedirect('/aliases/')
