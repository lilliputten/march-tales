from django.template.defaultfilters import register


@register.filter(name='math_min')
def math_min(arg1, arg2):
    try:
        return min(arg1, arg2)
    except (ValueError, TypeError):
        return ''
