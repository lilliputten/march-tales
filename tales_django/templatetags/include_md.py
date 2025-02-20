import traceback
import markdown

from django.template.defaultfilters import register
from django.template.loader import render_to_string

from core.helpers.errors import errorToString
from core.helpers.utils import debugObj
from core.logging import getDebugLogger

logger = getDebugLogger()

@register.simple_tag(takes_context=True)
def include_md(context, template_name):
    try:
        template = render_to_string(template_name)
        result = markdown.markdown(template)
        return result
    except Exception as err:
        sError = errorToString(err)
        sTraceback = str(traceback.format_exc())
        debugData = {
            'err': err,
            'traceback': sTraceback,
        }
        logger.error(f'[tick_api_view] Caught error {sError} (returning in response):\n{debugObj(debugData)}')
