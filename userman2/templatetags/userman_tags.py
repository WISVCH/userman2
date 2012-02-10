from django import template
from django.template.defaultfilters import stringfilter
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
        return "<a href='/userman2/aliases/" +value + "/'>" + value + "</a>"
    if user.Exists(value):
        return "<a href='/userman2/users/" +value + "/'>" + value + "</a>"
    return "<a href='/userman2/aliases?uid=" +value + "'>" + value + "</a>"
#    return value
    