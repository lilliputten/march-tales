import re
from django.template.defaultfilters import register


@register.filter(name='thumb_image_name_postfix')
def thumb_image_name_postfix(name: str, postfix: str = '-thumb'):
    """
    Make thumbnail image name from a static one:

    img.jpg -> img-thumb.jpg
    """
    thumb_name = re.sub(r'(\.[^.]+)$', postfix + r'\1', name)
    return thumb_name


@register.filter(name='thumb_image_name')
def thumb_image_name(name: str, prefix='thumbs/'):
    """
    Make thumbnail image name from a static one:

    img.jpg -> img-thumb.jpg
    """
    # arg_list = [arg.strip() for arg in prefix.split(',')]
    thumb_name = re.sub(r'/([^/]+)(\.[^.]+)$', '/' + prefix + r'\1\2', name)
    return thumb_name
