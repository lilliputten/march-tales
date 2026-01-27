import traceback

from django.conf import settings
from django.template.defaultfilters import register
from django.utils.translation import gettext_lazy as _

from core.helpers.errors import errorToString
from core.helpers.utils import debugObj
from core.logging import getDebugLogger
from tales_django.core.helpers import remove_html_tags
from tales_django.entities.ContentBlocks.models import ContentBlocks

logger = getDebugLogger()

_showDebug = False


@register.simple_tag
def content_block(name: str, default: str = ''):
    """
    Find and render a content block by name
    """
    content = ''
    try:
        if name:
            block = ContentBlocks.objects.filter(name=name).first()
            if block is not None and block.active:
                content = block.content
                if block.type != ContentBlocks.RICH_BLOCK:
                    content = remove_html_tags(content)
        if not content:
            content = _(default)
        if _showDebug and settings.DEBUG and content:
            content = name + ': ' + content
        return content
    except Exception as err:
        # DEBUG ONLY: Log detailed error information for debugging purposes
        # This helps track down issues with custom context getters
        sError = errorToString(err)
        sTraceback = str(traceback.format_exc())
        debugData = {
            'err': err,
            'traceback': sTraceback,
            'content': content,
        }
        logger.error(f'Context getter error: {sError}\n{debugObj(debugData)}')
        # raise err
        return content
