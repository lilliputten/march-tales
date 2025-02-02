import traceback

from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

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


class DefaultPagination(pagination.LimitOffsetPagination):
    default_limit = defaultTracksLimit


class TrackViewSet(viewsets.ModelViewSet):
    language = get_currrent_django_language()
    queryset = Track.objects.order_by('-published_at', f'title_{language}').all()
    serializer_class = TrackSerializer
    pagination_class = DefaultPagination

    def retrieve(self, request, *args, **kwargs):
        """
        Overrided single track retrieve method
        """
        instance = self.get_object()
        serializer = TrackSerializer(instance=instance)
        result = serializer.data
        return Response(result, headers=default_headers, content_type=content_type)

    def list(self, request):
        """
        Overrided track list retrieve method
        """
        limit = int(request.query_params.get('limit', defaultTracksLimit))
        offset = int(request.query_params.get('offset', defaultTracksOffset))

        # TODO: Extract sort/filter params and modify results below?

        language = get_currrent_django_language()
        query = Track.objects.filter(track_status='PUBLISHED').order_by('-published_at', f'title_{language}')
        subset = query.all()
        if query or limit:
            subset = query.all()[offset : offset + limit]

        result = {
            'count': len(query),
            'results': TrackSerializer(subset, many=True).data,
        }

        # result.update({
        #     'meta':{'api':'SmartTag'}
        # })

        return Response(result, headers=default_headers, content_type=content_type)

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
                return Response(
                    errorDetail, headers=default_headers, content_type=content_type, status=status.HTTP_403_FORBIDDEN
                )
            # Check session or csrf?
            if not session_key and not csrftoken:
                errorDetail = {'detail': _('Client session not found')}
                return Response(
                    errorDetail, headers=default_headers, content_type=content_type, status=status.HTTP_403_FORBIDDEN
                )

            track = get_object_or_404(Track, pk=pk)

            favorite_tracks = request.user.favorite_tracks
            if value:
                favorite_tracks.add(track)
            else:
                favorite_tracks.remove(track)

            favorite_track_ids = list(map(lambda it: it.id, favorite_tracks.all()))

            request.user.save()

            responseData = {'favorite_track_ids': favorite_track_ids}

            return Response(
                responseData, headers=default_headers, content_type=content_type, status=status.HTTP_200_OK, safe=True
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
            return Response(
                errorDetail,
                headers=default_headers,
                content_type=content_type,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        methods=['post'],
        url_path='increment-played-count',
        url_name='track-increment-played-count',
        detail=True,
        permission_classes=[permissions.BasePermission],
    )
    def incrementPlayedCount(self, request: Request, pk=None):
        try:
            session_key = request.session.session_key if request.session else None
            headers_csrftoken = request.headers.get('X-CSRFToken')
            meta_csrftoken = request.META.get('CSRF_COOKIE')
            csrftoken = meta_csrftoken if meta_csrftoken else headers_csrftoken

            # Check session or csrf?
            if not check_csrf(request):
                errorDetail = {'detail': _('Client session not found')}
                return Response(
                    errorDetail, headers=default_headers, content_type=content_type, status=status.HTTP_403_FORBIDDEN
                )

            track = get_object_or_404(Track, pk=pk)
            data = {
                'played_count': track.played_count + 1,
            }
            serializer = TrackSerializer(track, data=data, partial=True, context={'request': request})

            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    headers=default_headers,
                    content_type=content_type,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()

            return Response(serializer.data, headers=default_headers, content_type=content_type)
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
