from django.template.defaultfilters import register


@register.filter(name='str_starts')
def str_starts(value: str, check: str):
    return value.startswith(check)
