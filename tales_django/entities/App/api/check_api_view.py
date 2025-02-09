import traceback

# from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.middleware.csrf import CsrfViewMiddleware
from django.views.decorators.csrf import requires_csrf_token, csrf_protect, csrf_exempt

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
from tales_django.core.helpers.check_csrf import check_csrf

logger = getDebugLogger()

NOOP = lambda _: _

_ = lambda _: _


@csrf_exempt  # Will send json failure response manually
def check_api_view(request: Request):  # , *args, **kwargs):
    try:
        if request.method != 'POST':
            data = {'detail': _('Expected POST request')}
            return JsonResponse(data, status=status.HTTP_403_FORBIDDEN, safe=False)

        session_key = request.session.session_key if request.session else None
        headers_csrftoken = request.headers.get('X-CSRFToken')
        meta_csrftoken = request.META.get('CSRF_COOKIE')
        csrftoken = meta_csrftoken if meta_csrftoken else headers_csrftoken

        debugData = {
            'session_key': session_key,
            'headers_csrftoken': headers_csrftoken,
            'meta_csrftoken': meta_csrftoken,
            'csrftoken': csrftoken,
            'cyrillic': 'Тест',
        }
        debugStr = debugObj(debugData)
        logger.info(f'get\n{debugStr}')

        if not check_csrf(request):
            data = {'detail': _('Failed checking CSRF token')}
            return JsonResponse(data, status=status.HTTP_403_FORBIDDEN, safe=False)

        # # Check user is_authenticated?
        # if not request.user.is_authenticated:
        #     data = {'detail': _('User in not authenticated')}
        #     return JsonResponse(data, status=status.HTTP_403_FORBIDDEN, safe=False, json_dumps_params={'ensure_ascii': True}, content_type="application/json; charset=utf-8")
        # Check session or csrf?
        # if not session_key:
        #     data = {'detail': _('Client session not found')}
        #     return JsonResponse(data, status=status.HTTP_403_FORBIDDEN, safe=False, json_dumps_params={'ensure_ascii': True}, content_type="application/json; charset=utf-8")

        timestamp = getTimeStamp()
        data = {
            'PROJECT_INFO': PROJECT_INFO,
            'timestamp': timestamp,
            'checked': True,
            **debugData,  # DEBUG: Show debug data
        }
        return JsonResponse(
            data,
            status=status.HTTP_200_OK,
            json_dumps_params={'ensure_ascii': True},
            content_type='application/json; charset=utf-8',
        )
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
            json_dumps_params={'ensure_ascii': True},
            content_type='application/json; charset=utf-8',
        )
