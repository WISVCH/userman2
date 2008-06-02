from django import template
from django.template.defaultfilters import stringfilter
from userman.model import group
from userman.model import alias
from userman.model import user
register = template.Library()

@register.filter
@stringfilter
def groupname(value):
    return group.Groupname(value)

@register.filter
@stringfilter
def aliaslink(value):
    if alias.Exists(value):
        return "<a href='/aliases/" +value + "/'>" + value + "</a>"
    if user.Exists(value):
        return "<a href='/users/" +value + "/'>" + value + "</a>"
    return value