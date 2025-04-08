import math

from django.template.defaultfilters import register


@register.filter(name='math_ceil')
def math_ceil(value):
    try:
        return math.ceil(value)
    except (ValueError, TypeError):
        return ''
