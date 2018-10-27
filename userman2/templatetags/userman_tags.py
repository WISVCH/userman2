from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from userman2.model import alias
from userman2.model import group
from userman2.model import user

register = template.Library()


@register.filter
@stringfilter
def groupname(value):
    return group.Groupname(value)


@register.filter
@stringfilter
def aliaslink(value):
    if alias.Exists(value):
        return mark_safe("<a href='../../aliases/" + value + "/'>" + value + "</a>")
    if user.Exists(value):
        return mark_safe("<a href='../../users/" + value + "/'>" + value + "</a>")
    return mark_safe("<a href='../../aliases?uid=" + value + "'>" + value + "</a>")


@register.filter
def dienst2icon(dienst2Status):
    ret = ''
    if dienst2Status['status'] == 'error':
        ret = '<i class="fas fa-times-circle" style="color: red;"></i>'
    elif dienst2Status['status'] == 'warning':
        ret = '<i class="fas fa-exclamation-circle" style="color: orange"></i>'
    elif dienst2Status['status'] == 'success':
        ret = '<i class="fas fa-check-circle" style="color: green;"></i>'
    if 'href' in dienst2Status:
        ret = ' <a href="%s">%s</a>' % (dienst2Status['href'], ret)

    return mark_safe(ret)


@register.filter
def dienst2message(dienst2Status):
    ret = ''
    if 'error' in dienst2Status:
        ret = dienst2Status['error']
    elif 'message' in dienst2Status:
        ret = dienst2Status['message']
    if 'href' in dienst2Status:
        ret = '<a href="%s">%s</a>' % (dienst2Status['href'], ret)

    return mark_safe(ret)
