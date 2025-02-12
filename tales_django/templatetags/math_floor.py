from django.template.defaultfilters import register
import math


@register.filter(name='math_floor')
def math_floor(value):
    try:
        return math.floor(value)
    except (ValueError, TypeError):
        return ''
