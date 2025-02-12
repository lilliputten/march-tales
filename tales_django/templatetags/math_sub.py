from django.template.defaultfilters import register


@register.filter(name='math_sub')
def math_sub(value, arg):
    try:
        return value - arg
    except (ValueError, TypeError):
        return ''
