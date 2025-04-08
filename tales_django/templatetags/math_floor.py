import math

from django.template.defaultfilters import register


@register.filter(name='math_floor')
def math_floor(value):
    try:
        return math.floor(value)
    except (ValueError, TypeError):
        return ''
