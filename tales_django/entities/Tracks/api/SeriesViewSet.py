import traceback
from datetime import datetime

from django.db.models import QuerySet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request

from core.helpers.errors import errorToString
from core.helpers.utils import debugObj
from core.logging import getDebugLogger
from tales_django.core.constants.common_constants import data_content_type, default_headers
from tales_django.core.helpers.check_csrf import check_csrf
from tales_django.core.model_helpers import get_current_language

from ..models import Series, Track
from .series_serializers import SeriesSerializer

logger = getDebugLogger()


default_series_limit = 20
default_series_offset = 0


# NOTE: No `viewsets.ModelViewSet` -- we don't use modification methods, only our custom `retrieve` and `list` (see below)
class SeriesViewSet(viewsets.GenericViewSet):
    language = get_current_language()
    queryset = Series.objects.filter(is_visible=True).order_by(f'title_{language}').all()
    # serializer_class = SeriesSerializer
    # pagination_class = DefaultPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def retrieve(self, request, *args, **kwargs):
        """
        Overrided single series retrieve method
        """

        # Check session or csrf
        if not check_csrf(request):
            errorDetail = {'detail': _('Client session not found')}
            return JsonResponse(
                errorDetail,
                headers=default_headers,
                content_type=data_content_type,
                status=status.HTTP_403_FORBIDDEN,
            )

        full = int(request.query_params.get('full', '0'))

        instance = self.get_object()
        serializer = SeriesSerializer(instance=instance, full=full, context={'request': request})
        result = serializer.data
        return JsonResponse(result, headers=default_headers, content_type=data_content_type)

    def list(self, request):
        """
        Overrided series list retrieve method
        """

        try:
            # Check session or csrf
            if not check_csrf(request):
                errorDetail = {'detail': _('Client session not found')}
                return JsonResponse(
                    errorDetail,
                    headers=default_headers,
                    content_type=data_content_type,
                    status=status.HTTP_403_FORBIDDEN,
                )

            limit = int(request.query_params.get('limit', default_series_limit))
            offset = int(request.query_params.get('offset', default_series_offset))

            # Simple ordering by title in current language
            language = get_current_language()
            query = Series.objects.filter(is_visible=True).order_by(f'title_{language}')

            # Apply pagination: slice query if limit provided, otherwise get all results
            subset: QuerySet[Series] = query[offset : offset + limit] if limit else query.all()

            full = int(request.query_params.get('full', '0'))

            result = {
                'count': len(query),
                'results': SeriesSerializer(subset, many=True, full=full, context={'request': request}).data,
            }

            return JsonResponse(result, headers=default_headers, content_type=data_content_type)
        except Exception as err:
            sError = errorToString(err)
            sTraceback = str(traceback.format_exc())
            debugData = {
                'err': err,
                'traceback': sTraceback,
            }
            logger.error(f'Caught error {sError} (returning in response):\n{debugObj(debugData)}')
            errorDetail = {'detail': sError}
            return JsonResponse(
                errorDetail,
                headers=default_headers,
                content_type=data_content_type,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        methods=['get'],
        url_path='by-ids',
        url_name='series-by-ids',
        detail=False,
        permission_classes=[permissions.BasePermission],
    )
    def byIds(self, request: Request, pk=None):
        """
        Retrieve specific series by their IDs
        """

        # Check session or csrf
        if not check_csrf(request):
            errorDetail = {'detail': _('Client session not found')}
            return JsonResponse(
                errorDetail,
                headers=default_headers,
                content_type=data_content_type,
                status=status.HTTP_403_FORBIDDEN,
            )

        ids = request.query_params.get('ids')

        if not ids:
            return JsonResponse(
                {'details': _('Expected series indices list')},
                headers=default_headers,
                content_type=data_content_type,
                status=status.HTTP_400_BAD_REQUEST,
            )

        idsList: list[int] = []
        try:
            idsList = list(map(lambda s: int(s), ids.split(',')))
        except Exception as err:
            sError = _('Error parsing series indices list') + ': ' + errorToString(err)
            sTraceback = str(traceback.format_exc())
            debugData = {
                'err': err,
                'traceback': sTraceback,
            }
            logger.error(f'{sError}:\n{debugObj(debugData)}')
            errorDetail = {'detail': sError}
            return JsonResponse(
                errorDetail,
                headers=default_headers,
                content_type=data_content_type,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:
            limit = int(request.query_params.get('limit', default_series_limit))
            offset = int(request.query_params.get('offset', default_series_offset))

            debugData = {
                'idsList': idsList,
                'limit': limit,
                'offset': offset,
            }
            logger.info(f'[byIds]: params:\n{debugObj(debugData)}')

            language = get_current_language()

            query = Series.objects.filter(id__in=idsList, is_visible=True).order_by(f'title_{language}')
            subset = query.all()
            if limit:
                subset = query.all()[offset : offset + limit]

            full = int(request.query_params.get('full', '0'))

            result = {
                'count': len(query),
                'results': SeriesSerializer(subset, many=True, full=full, context={'request': request}).data,
            }

            return JsonResponse(
                result,
                headers=default_headers,
                content_type=data_content_type,
                json_dumps_params={'ensure_ascii': True},
            )

        except Exception as err:
            sError = errorToString(err)
            sTraceback = str(traceback.format_exc())
            debugData = {
                'err': err,
                'traceback': sTraceback,
            }
            logger.error(f'Caught error {sError} (returning in response):\n{debugObj(debugData)}')
            errorDetail = {'detail': sError}
            return JsonResponse(
                errorDetail,
                headers=default_headers,
                content_type=data_content_type,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        methods=['get'],
        url_path='with-promoted-tracks',
        url_name='series-with-promoted-tracks',
        detail=False,
        permission_classes=[permissions.BasePermission],
    )
    def withPromotedTracks(self, request: Request, pk=None):
        """
        Return series that have promoted tracks
        """

        # Check session or csrf
        if not check_csrf(request):
            errorDetail = {'detail': _('Client session not found')}
            return JsonResponse(
                errorDetail,
                headers=default_headers,
                content_type=data_content_type,
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            limit = int(request.query_params.get('limit', default_series_limit))
            offset = int(request.query_params.get('offset', default_series_offset))

            language = get_current_language()

            # Get series that have promoted tracks
            query = (
                Series.objects.filter(is_visible=True, tracks__track_status='PUBLISHED', tracks__promote=True)
                .distinct()
                .order_by(f'title_{language}')
            )

            subset = query.all()
            if limit:
                subset = query.all()[offset : offset + limit]

            full = int(request.query_params.get('full', '0'))

            result = {
                'count': len(query),
                'results': SeriesSerializer(subset, many=True, full=full, context={'request': request}).data,
            }

            return JsonResponse(result, headers=default_headers, content_type=data_content_type)
        except Exception as err:
            sError = errorToString(err)
            sTraceback = str(traceback.format_exc())
            debugData = {
                'err': err,
                'traceback': sTraceback,
            }
            logger.error(f'Caught error {sError} (returning in response):\n{debugObj(debugData)}')
            errorDetail = {'detail': sError}
            return JsonResponse(
                errorDetail,
                headers=default_headers,
                content_type=data_content_type,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
