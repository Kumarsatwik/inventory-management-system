from django import template
register = template.Library()


@register.filter(name='multiply')
def multiply(value):
    return int(value)*2
