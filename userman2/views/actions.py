from django.http import JsonResponse
from django.shortcuts import render

from userman2.model import action


def displayActions(request):
    return render(request, "actions.html")


def getActions(request):
    dn = request.GET.get("dn", None)
    filter_data = False
    if dn is not None:
        filter_data = {"affectedDN": dn}
    actions = action.GetAllActions(filter_data)
    ret = []

    def transform_action(a):
        children = list(map(transform_action, filter(lambda x: x.parentDN == a.dn, actions)))
        return {
            "dn": a.dn,
            "affectedDN": a.affectedDN,
            "name": a.actionName,
            "description": a.description,
            "locked": a.locked,
            "host": a.host,
            "children": children,
        }

    for a in actions:
        if a.parentDN:
            continue
        ret.append(transform_action(a))
    return JsonResponse({"actions": ret})
