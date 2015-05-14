from django import template

from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from settings import STATIC_URL

from userman2.model import group

from userman2.model import alias
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
def dienst2render(dienst2Status):
    if 'error' in dienst2Status:
        ret = '<img src="%scircle_blue.png" title="Error: %s" width="16" height="16" />' % (STATIC_URL, dienst2Status['error'])
    else:
        ret = '<img src="%s%s.png" title="%s" width="16" height="16" />' % (
        STATIC_URL, dienst2Status['status'], dienst2Status['message'])
        if 'href' in dienst2Status:
            ret = '<a href="%s">%s</a>' % (dienst2Status['href'], ret)

    return mark_safe(ret)

