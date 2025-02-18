from django.template.defaultfilters import register


@register.filter(name='math_max')
def math_max(arg1, arg2):
    try:
        return max(arg1, arg2)
    except (ValueError, TypeError):
        return ''
