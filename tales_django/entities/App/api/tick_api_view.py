import traceback

# from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, get_token

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
from rest_framework import permissions

from core.appEnv import PROJECT_INFO
from core.helpers.errors import errorToString
from core.helpers.time import getTimeStamp
from core.helpers.utils import debugObj
from core.logging import getDebugLogger


logger = getDebugLogger()

_ = lambda _: _


@csrf_exempt  # CSRF check isn't required here: should answer even for 'clear' requests (with a brand new token)
def tick_api_view(request: Request):   # , *args, **kwargs):
    """
    The method could be used to initialize a csrf session (obtaining fresh token if it has been absent).
    """
    try:
        if request.method != 'POST' and request.method != 'GET':
            data = {'detail': _('Expected POST or GET request')}
            return JsonResponse(data, status=status.HTTP_403_FORBIDDEN, safe=False)

        session_key = request.session.session_key if request.session else None
        headers_csrftoken = request.headers.get('X-CSRFToken')
        meta_csrftoken = request.META.get('CSRF_COOKIE')
        csrftoken = meta_csrftoken if meta_csrftoken else headers_csrftoken

        # NOTE: Ensure the CSRF token will be regenerated
        response_csrftoken = csrftoken if csrftoken else get_token(request)

        debugData = {
            'session_key': session_key,
            'headers_csrftoken': headers_csrftoken,
            'meta_csrftoken': meta_csrftoken,
            'csrftoken': csrftoken,
            'response_csrftoken': response_csrftoken,
        }
        debugStr = debugObj(debugData)
        logger.info(f'get\n{debugStr}')

        timestamp = getTimeStamp()
        data = {
            'PROJECT_INFO': PROJECT_INFO,
            'timestamp': timestamp,
            'checked': True,
            **debugData,  # DEBUG: Show debug data
        }
        response = JsonResponse(data, status=status.HTTP_200_OK)
        # XXX: Test multiple cookies processing
        # response.set_cookie(key='key1', value='value1', max_age=3600)
        # response.set_cookie(key='key2', value='value2', max_age=600)
        return response
    except Exception as err:
        sError = errorToString(err)
        sTraceback = str(traceback.format_exc())
        debugData = {
            'err': err,
            'traceback': sTraceback,
        }
        logger.error(f'Caught error {sError} (returning in response):\n{debugObj(debugData)}')
        return JsonResponse(
            {
                'detail': sError,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            safe=False,
        )
