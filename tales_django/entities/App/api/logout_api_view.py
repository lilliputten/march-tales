import traceback

# from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, get_token
from django.conf import settings

from rest_framework.request import Request
from rest_framework import status

from core.appEnv import PROJECT_INFO
from core.helpers.errors import errorToString
from core.helpers.time import getTimeStamp
from core.helpers.utils import debugObj
from core.logging import getDebugLogger


logger = getDebugLogger()

_ = lambda _: _


@csrf_exempt  # CSRF check isn't required here: should answer even for 'clear' requests (with a brand new token)
def logout_api_view(request: Request):  # , *args, **kwargs):
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

        debugData = {
            'projectInfo': PROJECT_INFO,
            'androidAppVersion': settings.APK_DOWNLOAD_VERSION,
            'is_authenticated': is_authenticated,
        }
        debugStr = debugObj(debugData)
        logger.info(f'[signout_api_view] get\n{debugStr}')

        if not user.is_authenticated:
            data = {
                'details': 'Already logged out',
                **debugData,  # DEBUG: Show debug data
            }
            response = JsonResponse(
                data,
                status=status.HTTP_200_OK,
                json_dumps_params={'ensure_ascii': True},
                content_type='application/json; charset=utf-8',
            )

        session_key = request.session.session_key if request.session else None

        request.session.delete()

        # request.ser.auth_token.delete()
        # s = SessionStore(session_key=session_key)
        # s.delete()

        data = {
            'details': 'Successfully logged out',
            'session_key': session_key,
            **debugData,  # DEBUG: Show debug data
        }
        response = JsonResponse(
            data,
            status=status.HTTP_200_OK,
            json_dumps_params={'ensure_ascii': True},
            content_type='application/json; charset=utf-8',
        )
        return response
    except Exception as err:
        sError = errorToString(err)
        sTraceback = str(traceback.format_exc())
        debugData = {
            'err': err,
            'traceback': sTraceback,
        }
        logger.error(f'[signout_api_view] Caught error {sError} (returning in response):\n{debugObj(debugData)}')
        return JsonResponse(
            {
                'detail': sError,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            safe=False,
            json_dumps_params={'ensure_ascii': True},
            content_type='application/json; charset=utf-8',
        )
