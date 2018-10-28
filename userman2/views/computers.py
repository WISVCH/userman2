from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.cache import cache_control

from userman2.forms.computer import *
from userman2.model import computer


@cache_control(no_cache=True, must_revalidate=True)
def displayComputers(request):
    computers = computer.getAllComputers()
    count = 0
    for c in computers:
        count += 1

    return render(request, 'computers.html', {'computers': computers, 'count': count})


@cache_control(no_cache=True, must_revalidate=True)
def addComputer(request):
    if request.method == 'POST':
        form = AddComputerForm(request.POST)
        if form.is_valid():
            uid = form.cleaned_data['uid'] + '$'
            if computer.Exists(uid):
                raise Http404
            newComputer = computer.Add(uid)

            return HttpResponseRedirect('/computers/')
    else:
        form = AddComputerForm()

    return render(request, 'form.html', {'form': form, 'uid': "computers"})


@cache_control(no_cache=True, must_revalidate=True)
def rmComputer(request, cn):
    try:
        computerObj = computer.FromUID(cn)
    except Exception as e:
        raise Http404

    computerObj.connectRoot()
    computerObj.remove()
    return HttpResponseRedirect('/computers/')
