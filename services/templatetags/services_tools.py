from django import template
register = template.Library()


@register.filter(name='index')
def index(list, i):
    return list[i - 1]
