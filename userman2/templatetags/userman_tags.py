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
        return mark_safe("<a href='/aliases/" + value + "'>" + value + "</a>")
    if user.Exists(value):
        return mark_safe("<a href='/users/" + value + "'>" + value + "</a>")
    return mark_safe("<a href='/aliases?uid=" + value + "'>" + value + "</a>")
