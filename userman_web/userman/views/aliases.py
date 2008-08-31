from userman.model import alias
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.cache import cache_control
from django.conf import settings

from userman.forms.alias import *

@cache_control(no_cache=True, must_revalidate=True)
def displayAliases(request):
    if (request.GET):
        form = AliasForm(request.GET)
        if form.is_valid():
            aliases = alias.getAllAliases(form.clean_data)
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
    return HttpResponseRedirect(settings.USERMAN_PREFIX + '/aliases/' + aliasObj.cn + '/')

@cache_control(no_cache=True, must_revalidate=True)
def adduser(request, cn):
    try:
        aliasObj = alias.fromCN(cn)
    except Exception, e:
        raise Http404
    
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            aliasObj.connectRoot()
            if form.clean_data['uid']: aliasObj.addMember(str(form.clean_data['uid']))
            elif form.clean_data['alias']: aliasObj.addMember(str(form.clean_data['alias']))
            elif form.clean_data['email']: aliasObj.addMember(str(form.clean_data['email']))
            return HttpResponseRedirect(settings.USERMAN_PREFIX + '/aliases/' + aliasObj.cn + '/')
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
            if alias.Exists(form.clean_data['common_name']):
                raise Http404
            alias.Add(parent, str(form.clean_data['common_name']))
            return HttpResponseRedirect(settings.USERMAN_PREFIX + '/aliases/' + form.clean_data['common_name'] + '/')
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
    return HttpResponseRedirect(settings.USERMAN_PREFIX + '/aliases/')
    