from django.template.defaultfilters import register
from django.utils.translation import gettext_lazy as _

from tales_django.core.helpers import remove_html_tags
from tales_django.entities.ContentBlocks.models import ContentBlocks


@register.simple_tag
def content_block(name: str, default: str = ''):
    """
    Find and render a content block by name
    """
    if name:
        block = ContentBlocks.objects.filter(name=name).first()
        if block is not None:
            content = block.content
            if block.type != ContentBlocks.RICH_BLOCK:
                content = remove_html_tags(content)
            return content
    return _(default)
