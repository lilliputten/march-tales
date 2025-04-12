import traceback

from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.request import Request

from core.helpers.errors import errorToString
from core.helpers.utils import debugObj
from core.logging import getDebugLogger
from tales_django.core.helpers.check_csrf import check_csrf
from tales_django.core.pages.get_favorites_list_context import get_favorites_ids

logger = getDebugLogger()


@csrf_exempt  # Will send json failure response manually
def sync_user_tracks_api_view(request: Request):
    try:
        if request.method != 'POST':
            data = {'detail': _('Expected POST request')}
            return JsonResponse(
                data,
                status=status.HTTP_403_FORBIDDEN,
                safe=False,
                json_dumps_params={'ensure_ascii': True},
                content_type='application/json; charset=utf-8',
            )

        if not check_csrf(request):
            data = {'detail': _('Failed checking CSRF token')}
            return JsonResponse(data, status=status.HTTP_403_FORBIDDEN, safe=False)

        # Check user is_authenticated?
        if not request.user.is_authenticated:
            data = {'detail': _('User in not authenticated')}
            return JsonResponse(
                data,
                status=status.HTTP_403_FORBIDDEN,
                safe=False,
                json_dumps_params={'ensure_ascii': True},
                content_type='application/json; charset=utf-8',
            )

        list = request.data.get('list')

        if list is None or not isinstance(list, list):
            data = {'detail': _('Expected objects list')}
            return JsonResponse(
                data,
                status=status.HTTP_400_BAD_REQUEST,
                safe=False,
                json_dumps_params={'ensure_ascii': True},
                content_type='application/json; charset=utf-8',
            )

        debugData = {
            'list': list,
        }
        debugStr = debugObj(debugData)
        logger.info(f'[sync_user_tracks_api_view] Got data\n{debugStr}')

        # TODO: Sync UserTrack list

        data = {
            'items': list,
            # **debugData,  # DEBUG: Show debug data
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
