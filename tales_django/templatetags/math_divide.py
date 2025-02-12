from django.template.defaultfilters import register


@register.filter(name='math_divide')
def math_divide(value, arg):
    try:
        return float(value) / float(arg) if float(arg) != 0 else ''
    except (ValueError, TypeError):
        return ''
