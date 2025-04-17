import traceback

from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.request import Request

from core.helpers.errors import errorToString
from core.helpers.utils import debugObj
from core.logging import getDebugLogger
from tales_django.core.constants.common_constants import data_content_type
from tales_django.core.helpers import check_csrf
from tales_django.core.pages import get_recents_context

logger = getDebugLogger()


@csrf_exempt  # CSRF check isn't required here: should answer even for 'clear' requests (with a brand new token)
def recents_api_view(request: Request):  # , *args, **kwargs):
    """
    Get lists of recent/popular/other entries.
    """
    try:
        if request.method != 'POST' and request.method != 'GET':
            data = {'detail': _('Expected POST or GET request')}
            return JsonResponse(
                data,
                status=status.HTTP_403_FORBIDDEN,
                safe=False,
                json_dumps_params={'ensure_ascii': True},
                content_type=data_content_type,
            )

        if not check_csrf(request):
            data = {'detail': _('Failed checking CSRF token')}
            return JsonResponse(data, status=status.HTTP_403_FORBIDDEN, safe=False)

        context = {
            **get_recents_context(request, serialize=True),
        }

        debugData = {
            'context': context,
        }
        debugStr = debugObj(debugData)
        logger.info(f'[recents_api_view] get\n{debugStr}')

        data = {
            **context,
            **debugData,  # DEBUG: Show debug data
        }
        response = JsonResponse(
            data,
            status=status.HTTP_200_OK,
            json_dumps_params={'ensure_ascii': True},
            content_type=data_content_type,
        )
        return response
    except Exception as err:
        sError = errorToString(err)
        sTraceback = str(traceback.format_exc())
        debugData = {
            'err': err,
            'traceback': sTraceback,
        }
        logger.error(f'[recents_api_view] Caught error {sError} (returning in response):\n{debugObj(debugData)}')
        return JsonResponse(
            {
                'detail': sError,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            safe=False,
            json_dumps_params={'ensure_ascii': True},
            content_type=data_content_type,
        )
