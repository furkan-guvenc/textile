from django import template

register = template.Library()


@register.filter()
def filter_range(value):
    return range(value)
