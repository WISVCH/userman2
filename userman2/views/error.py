from django.shortcuts import render


def Error(request, message):
    return render(request, "error.html", context={"msg": message}, status=500)
