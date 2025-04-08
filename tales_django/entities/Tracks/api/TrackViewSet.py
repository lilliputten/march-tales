import traceback

from django.db.models import QuerySet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request

from core.helpers.errors import errorToString
from core.helpers.utils import debugObj
from core.logging import getDebugLogger
from tales_django.core.helpers.check_csrf import check_csrf
from tales_django.core.model_helpers import get_current_language

from ..models import Track
from .common_constants import content_type, default_headers
from .track_constants import default_tracks_limit, default_tracks_offset
from .track_filters import (get_search_filter_args, get_track_filter_kwargs,
                            get_track_order_args)
from .track_serializers import TrackSerializer

logger = getDebugLogger()


# NOTE: No `viewsets.ModelViewSet` -- we don't use modification methods, only our custom `retrieve` and `list` (see below)
class TrackViewSet(viewsets.GenericViewSet):
    language = get_current_language()
    queryset = Track.objects.order_by('-published_at', f'title_{language}').all()
    # serializer_class = TrackSerializer
    # pagination_class = DefaultPagination

    def retrieve(self, request, *args, **kwargs):
        """
        Overrided single track retrieve method
        """

        # Check session or csrf
        if not check_csrf(request):
            errorDetail = {'detail': _('Client session not found')}
            return JsonResponse(
                errorDetail, headers=default_headers, content_type=content_type, status=status.HTTP_403_FORBIDDEN
            )

        full = int(request.query_params.get('full', '0'))

        instance = self.get_object()
        serializer = TrackSerializer(instance=instance, full=full)
        result = serializer.data
        return JsonResponse(result, headers=default_headers, content_type=content_type)

    def list(self, request):
        """
        Overrided track list retrieve method
        """

        try:
            # Check session or csrf
            if not check_csrf(request):
                errorDetail = {'detail': _('Client session not found')}
                return JsonResponse(
                    errorDetail, headers=default_headers, content_type=content_type, status=status.HTTP_403_FORBIDDEN
                )

            limit = int(request.query_params.get('limit', default_tracks_limit))
            offset = int(request.query_params.get('offset', default_tracks_offset))

            order_args = get_track_order_args(
                request
            )  # Retrieves ordering parameters from the request to determine how tracks should be sorted
            filter_kwargs = get_track_filter_kwargs(
                request
            )  # Gets filter keyword arguments from the request for filtering tracks based on specific criteria
            filter_args = get_search_filter_args(
                request
            )  # Extracts search-related filter arguments from the request for text-based searching

            # Previous straightforward approach, keeping for reference
            # query = Track.objects.filter(track_status='PUBLISHED').order_by('-published_at', f'title_{language}')
            # Build filtered and ordered query with distinct results
            query = Track.objects.filter(*filter_args, **filter_kwargs).distinct().order_by(*order_args)
            # Apply pagination: slice query if limit provided, otherwise get all results
            subset: QuerySet[Track] = query[offset : offset + limit] if limit else query.all()

            full = int(request.query_params.get('full', '0'))

            result = {
                'count': len(query),
                'results': TrackSerializer(subset, many=True, full=full).data,
            }

            # result.update({
            #     'meta':{'api':'SmartTag'}
            # })

            return JsonResponse(result, headers=default_headers, content_type=content_type)
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
                content_type=content_type,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        methods=['get'],
        url_path='by-ids',
        url_name='track-by-ids',
        detail=False,
        permission_classes=[permissions.BasePermission],
    )
    def byIds(self, request: Request, pk=None):
        host = request.headers.get('Host')
        referer = request.headers.get('Referer')
        session_key = request.session.session_key if request.session else None
        headers_csrftoken = request.headers.get('X-CSRFToken')
        meta_csrftoken = request.META.get('CSRF_COOKIE')
        csrftoken = meta_csrftoken if meta_csrftoken else headers_csrftoken

        debugData = {
            'host': host,
            'referer': referer,
            'session_key': session_key,
            'headers_csrftoken': headers_csrftoken,
            'meta_csrftoken': meta_csrftoken,
            'csrftoken': csrftoken,
        }
        logger.info(f'[byIds]: DEBUG:\n{debugObj(debugData)}')

        # Check session or csrf?
        if not check_csrf(request):
            errorDetail = {'detail': _('Client session not found')}
            return JsonResponse(
                errorDetail, headers=default_headers, content_type=content_type, status=status.HTTP_403_FORBIDDEN
            )

        ids = request.query_params.get('ids')

        if not ids:
            return JsonResponse(
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
            return JsonResponse(
                errorDetail,
                headers=default_headers,
                content_type=content_type,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:
            limit = int(request.query_params.get('limit', default_tracks_limit))
            offset = int(request.query_params.get('offset', default_tracks_offset))

            debugData = {
                'idsList': idsList,
                'limit': limit,
                'offset': offset,
            }
            logger.info(f'[list]: params:\n{debugObj(debugData)}')

            # language = get_current_language()

            # TODO: Extract sort/filter params and modify results below?
            query = Track.objects.filter(id__in=idsList, track_status='PUBLISHED')
            # .order_by('-published_at', f'title_{language}')
            subset = query.all()
            if limit:
                subset = query.all()[offset : offset + limit]

            full = int(request.query_params.get('full', '0'))

            result = {
                'count': len(query),
                'results': TrackSerializer(subset, many=True, full=full).data,
            }

            return JsonResponse(
                result,
                headers=default_headers,
                content_type=content_type,
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
                content_type=content_type,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        methods=['get'],
        url_path='next',
        url_name='track-next',
        detail=True,
        permission_classes=[permissions.BasePermission],
    )
    def next(self, request: Request, pk=None):
        """
        Find next track in the current query set (according to filter parameters).
        """
        try:

            session_key = request.session.session_key if request.session else None
            csrftoken = request.headers.get('X-CSRFToken')

            # Check session or csrf?
            if not session_key and not csrftoken:
                errorDetail = {'detail': _('Client session not found')}
                return JsonResponse(
                    errorDetail, headers=default_headers, content_type=content_type, status=status.HTTP_403_FORBIDDEN
                )

            track = get_object_or_404(Track, pk=pk)

            order_args = get_track_order_args(request)
            filter_kwargs = get_track_filter_kwargs(request)
            filter_args = get_search_filter_args(request)

            query = Track.objects.filter(*filter_args, **filter_kwargs).distinct().order_by(*order_args)
            ids = list(query.values_list('id', flat=True))
            idx = ids.index(track.id)
            next_idx = (idx + 1) % len(ids)

            # TODO: Find next track
            next_track = query[next_idx]

            debugData = {
                'ids': ids,
                'idx': idx,
                'track.id': track.id,
                'track': track,
                'query': query,
            }
            logger.info(f'[next]: params:\n{debugObj(debugData)}')

            full = int(request.query_params.get('full', '0'))

            serializer = TrackSerializer(instance=next_track, full=full)
            result = serializer.data
            return JsonResponse(result, headers=default_headers, content_type=content_type)

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
                content_type=content_type,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        methods=['post', 'get'],
        url_path='toggle-favorite',
        url_name='track-toggle-favorite',
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def toggleFavorite(self, request: Request, pk=None):
        try:
            value = request.data.get('value')

            session_key = request.session.session_key if request.session else None
            csrftoken = request.headers.get('X-CSRFToken')

            # Check user is_authenticated?
            if not request.user.is_authenticated:
                errorDetail = {'detail': _('User in not authenticated')}
                return JsonResponse(
                    errorDetail, headers=default_headers, content_type=content_type, status=status.HTTP_403_FORBIDDEN
                )
            # Check session or csrf?
            if not session_key and not csrftoken:
                errorDetail = {'detail': _('Client session not found')}
                return JsonResponse(
                    errorDetail, headers=default_headers, content_type=content_type, status=status.HTTP_403_FORBIDDEN
                )

            track = get_object_or_404(Track, pk=pk)

            debugData = {
                'value': value,
                'track.id': track.id,
            }
            logger.info(f'[toggleFavorite]: params:\n{debugObj(debugData)}')

            favorite_tracks = request.user.favorite_tracks
            if value:
                favorite_tracks.add(track)
            else:
                favorite_tracks.remove(track)

            favorite_track_ids = list(map(lambda it: it.id, favorite_tracks.all()))

            request.user.save()

            responseData = {'favorite_track_ids': favorite_track_ids}

            return JsonResponse(
                responseData, headers=default_headers, content_type=content_type, status=status.HTTP_200_OK
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
                content_type=content_type,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # @csrf_exempt
    @action(
        methods=['post'],
        url_path='increment-played-count',
        url_name='track-increment-played-count',
        detail=True,
        permission_classes=[permissions.BasePermission],
    )
    def incrementPlayedCount(self, request: Request, pk=None):
        try:
            host = request.headers.get('Host')
            referer = request.headers.get('Referer')
            session_key = request.session.session_key if request.session else None
            headers_csrftoken = request.headers.get('X-CSRFToken')
            meta_csrftoken = request.META.get('CSRF_COOKIE')
            csrftoken = meta_csrftoken if meta_csrftoken else headers_csrftoken

            debugData = {
                'host': host,
                'referer': referer,
                'session_key': session_key,
                'headers_csrftoken': headers_csrftoken,
                'meta_csrftoken': meta_csrftoken,
                'csrftoken': csrftoken,
            }
            logger.info(f'[incrementPlayedCount]: DEBUG:\n{debugObj(debugData)}')

            # Check session or csrf?
            if not check_csrf(request):
                errorDetail = {'detail': _('Client session not found')}
                return JsonResponse(
                    errorDetail, headers=default_headers, content_type=content_type, status=status.HTTP_403_FORBIDDEN
                )

            track = get_object_or_404(Track, pk=pk)
            data = {
                'played_count': track.played_count + 1,
            }

            full = int(request.query_params.get('full', '0'))

            serializer = TrackSerializer(track, data=data, full=full, partial=True, context={'request': request})

            if not serializer.is_valid():
                return JsonResponse(
                    serializer.errors,
                    headers=default_headers,
                    content_type=content_type,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()

            return JsonResponse(serializer.data, headers=default_headers, content_type=content_type)
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
                content_type=content_type,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
