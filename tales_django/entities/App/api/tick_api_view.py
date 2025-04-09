import traceback

from django.conf import settings

# from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, get_token
from rest_framework import status
from rest_framework.request import Request

from core.appEnv import PROJECT_INFO
from core.helpers.errors import errorToString
from core.helpers.time import getTimeStamp
from core.helpers.utils import debugObj
from core.logging import getDebugLogger

logger = getDebugLogger()

_ = lambda _: _


@csrf_exempt  # CSRF check isn't required here: should answer even for 'clear' requests (with a brand new token)
def tick_api_view(request: Request):  # , *args, **kwargs):
    """
    The method could be used to initialize a csrf session (obtaining fresh token if it has been absent).
    """
    try:
        if request.method != 'POST' and request.method != 'GET':
            data = {'detail': _('Expected POST or GET request')}
            return JsonResponse(
                data,
                status=status.HTTP_403_FORBIDDEN,
                safe=False,
                json_dumps_params={'ensure_ascii': True},
                content_type='application/json; charset=utf-8',
            )

        user = request.user if request else None
        is_authenticated = user.is_authenticated if user else False

        host = request.headers.get('Host')
        referer = request.headers.get('Referer')
        session_key = request.session.session_key if request.session else None
        headers_csrftoken = request.headers.get('X-CSRFToken')
        meta_csrftoken = request.META.get('CSRF_COOKIE')
        csrftoken = meta_csrftoken if meta_csrftoken else headers_csrftoken

        # NOTE: Ensure the CSRF token will be regenerated
        response_csrftoken = csrftoken if csrftoken else get_token(request)

        debugData = {
            'host': host,
            'referer': referer,
            'session_key': session_key,
            'headers_csrftoken': headers_csrftoken,
            'meta_csrftoken': meta_csrftoken,
            'csrftoken': csrftoken,
            'response_csrftoken': response_csrftoken,
            # 'cyrillic': 'Тест',
            # 'user': user,
        }
        debugStr = debugObj(debugData)
        logger.info(f'[tick_api_view] get\n{debugStr}')

        timestamp = getTimeStamp()
        data = {
            'PROJECT_INFO': PROJECT_INFO,  # TODO: Remoe it later in favor of below `projectInfo`
            'projectInfo': PROJECT_INFO,
            'androidAppVersion': settings.APK_DOWNLOAD_VERSION,
            'timestamp': timestamp,
            'is_authenticated': is_authenticated,
            # 'auth_token': user.auth_token,
            'user_id': user.id if is_authenticated else None,
            'user_name': user.get_name_or_email() if is_authenticated else None,
            'user_email': user.email if is_authenticated else None,  # TODO: Remove it later in favor of `user_id`
            'checked': True,
            **debugData,  # DEBUG: Show debug data
        }
        response = JsonResponse(
            data,
            status=status.HTTP_200_OK,
            json_dumps_params={'ensure_ascii': True},
            content_type='application/json; charset=utf-8',
        )
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
        logger.error(f'[tick_api_view] Caught error {sError} (returning in response):\n{debugObj(debugData)}')
        return JsonResponse(
            {
                'detail': sError,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            safe=False,
            json_dumps_params={'ensure_ascii': True},
            content_type='application/json; charset=utf-8',
        )
