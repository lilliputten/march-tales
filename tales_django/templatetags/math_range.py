from django.template.defaultfilters import register


@register.filter(name='math_range')
def math_range(start, end):
    try:
        return range(start, end)
    except (ValueError, TypeError):
        return ''
