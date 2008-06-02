from userman.model import alias
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.cache import cache_control

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
    
    return render_to_response('groupsaliases.html', {'groups': aliases, 'form': form})


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
    except Exception, e:
        raise Http404
    
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            aliasObj.connectRoot()
            aliasObj.addMember(str(form.clean_data["user"]))
            return HttpResponseRedirect('/aliases/' + aliasObj.cn + '/')
    else:
        form = AddUserForm()

    return render_to_response('form.html', {'form': form, 'uid': aliasObj.cn})
