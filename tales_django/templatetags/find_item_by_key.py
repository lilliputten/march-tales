from django.db.models import Q, QuerySet
from django.template.defaultfilters import register


@register.simple_tag
def find_item_by_key(items: list | QuerySet, key: str, value: any):
    """
    Find object (!) in the QuerySet or in the list by object field
    """
    if items is None or not len(items):
        return None
    result = None
    if isinstance(items, QuerySet):
        result = items.filter(Q(**{key: value}))
    else:
        result = list(filter(lambda it: it[key] == value, items))
    if not result or not len(result):
        return None
    return result[0]
