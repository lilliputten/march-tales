import traceback
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
from rest_framework import permissions

from core.helpers.errors import errorToString
from core.helpers.time import getTimeStamp
from core.helpers.utils import debugObj
from core.logging import getDebugLogger


logger = getDebugLogger()


class CheckApiView(views.APIView):
    permission_classes = [
        permissions.BasePermission,
        # permissions.IsAuthenticated,
    ]

    def get(self, request: Request):   # , *args, **kwargs):
        try:
            session_key = request.session.session_key if request.session else None
            csrftoken = request.headers.get('X-CSRFToken')

            logger.info(f'get: session_key: {session_key} csrftoken: {csrftoken}')

            # # Check user is_authenticated?
            # if not request.user.is_authenticated:
            #     data = {'detail': _('User in not authenticated')}
            #     return JsonResponse(data, status=status.HTTP_403_FORBIDDEN, safe=False)
            # Check session or csrf?
            if not session_key and not csrftoken:
                data = {'detail': _('Client session not found')}
                return JsonResponse(data, status=status.HTTP_403_FORBIDDEN, safe=False)

            timestamp = getTimeStamp()
            data = {
                'timestamp': timestamp,
                'checked': True,
            }
            return Response(data, status=status.HTTP_200_OK)
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
