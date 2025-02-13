from django.template.defaultfilters import register


@register.filter(name='math_round')
def math_round(value):
    try:
        return round(value)
    except (ValueError, TypeError):
        return ''
