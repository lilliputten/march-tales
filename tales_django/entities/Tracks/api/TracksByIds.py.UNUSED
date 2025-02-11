import traceback

from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework import pagination

from core.helpers.errors import errorToString
from core.helpers.utils import debugObj
from core.logging import getDebugLogger

from tales_django.core.helpers.check_csrf import check_csrf
from tales_django.core.model_helpers import get_currrent_django_language

from .track_serializers import TrackSerializer

from ..models import Track

logger = getDebugLogger()


defaultTracksLimit = 5
defaultTracksOffset = 0

content_type = 'application/json; charset=utf-8'
default_headers = {
    # 'Content-Type': content_type,
}


class TracksByIds(viewsets.GenericViewSet):
    def list(self, request):
        """
        Overrided track list retrieve method
        """

        # Check session or csrf
        if not check_csrf(request):
            errorDetail = {'detail': _('Client session not found')}
            return Response(
                errorDetail, headers=default_headers, content_type=content_type, status=status.HTTP_403_FORBIDDEN
            )

        ids = request.query_params.get('ids')

        if not ids:
            return Response(
                {'details': _('Expected track indices list')},
                headers=default_headers,
                content_type=content_type,
                status=status.HTTP_400_BAD_REQUEST,
            )

        idsList: list[int] = []
        try:
            idsList = list(map(lambda s: int(s), ids.split(',')))
        except Exception as err:
            sError = _('Error parsing track indices list') + ': ' + errorToString(err)
            sTraceback = str(traceback.format_exc())
            debugData = {
                'err': err,
                'traceback': sTraceback,
            }
            logger.error(f'{sError}:\n{debugObj(debugData)}')
            errorDetail = {'detail': sError}
            return Response(
                errorDetail,
                headers=default_headers,
                content_type=content_type,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:
            limit = int(request.query_params.get('limit', defaultTracksLimit))
            offset = int(request.query_params.get('offset', defaultTracksOffset))

            debugData = {
                'idsList': idsList,
                'limit': limit,
                'offset': offset,
            }
            logger.info(f'[list]: params:\n{debugObj(debugData)}')

            language = get_currrent_django_language()
            # TODO: Extract sort/filter params and modify results below?
            query = Track.objects.filter(id__in=idsList, track_status='PUBLISHED')
            # .order_by('-published_at', f'title_{language}')
            subset = query.all()
            if offset or limit:
                subset = query.all()[offset : offset + limit]

            result = {
                'count': len(query),
                'results': TrackSerializer(subset, many=True).data,
            }

            return Response(result, headers=default_headers, content_type=content_type)
        except Exception as err:
            sError = errorToString(err)
            sTraceback = str(traceback.format_exc())
            debugData = {
                'err': err,
                'traceback': sTraceback,
            }
            logger.error(f'Caught error {sError} (returning in response):\n{debugObj(debugData)}')
            errorDetail = {'detail': sError}
            return Response(
                errorDetail,
                headers=default_headers,
                content_type=content_type,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
