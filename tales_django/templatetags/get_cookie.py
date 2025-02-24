import traceback

from django.template.defaultfilters import register

from core.helpers.errors import errorToString
from core.helpers.utils import debugObj
from core.logging import getDebugLogger

logger = getDebugLogger()


@register.simple_tag(takes_context=True)
def get_cookie(context, name):
    try:
        request = context['request']
        result = request.COOKIES.get(name)
        return result
    except Exception as err:
        sError = errorToString(err)
        sTraceback = str(traceback.format_exc())
        debugData = {
            'err': err,
            'traceback': sTraceback,
        }
        logger.error(f'[get_cookie] Caught error {sError} (returning in response):\n{debugObj(debugData)}')
