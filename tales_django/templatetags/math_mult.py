from django.template.defaultfilters import register


@register.filter(name='math_mult')
def math_mult(value, arg):
    try:
        return value * arg
    except (ValueError, TypeError):
        return ''
