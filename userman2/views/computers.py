from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.cache import cache_control

from userman2.forms.computer import *
from userman2.model import computer


def displayComputers(request):
    computers = computer.getAllComputers()
    count = len(computers)
    return render(request, "computers.html", {"computers": computers, "count": count})


def addComputer(request):
    if request.method == "POST":
        form = AddComputerForm(request.POST)
        if form.is_valid():
            uid = form.cleaned_data["uid"] + "$"
            if not computer.Exists(uid):
                computer.Add(uid)
            return HttpResponseRedirect("/computers")
    else:
        form = AddComputerForm()

    return render(request, "form.html", {"form": form, "uid": "computers"})


def rmComputer(request, cn):
    if request.method != "POST":
        raise Http404

    try:
        computerObj = computer.FromUID(cn)
    except:
        raise Http404

    computerObj.connectRoot()
    computerObj.remove()
    return HttpResponseRedirect("/computers")
