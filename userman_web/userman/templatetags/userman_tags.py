from django import template
from django.template.defaultfilters import stringfilter
from userman.model import group

register = template.Library()

@register.filter
@stringfilter
def groupname(value):
    return group.groupname(value)
