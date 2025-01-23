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

from .track_serializers import TrackSerializer

from ..models import Track

logger = getDebugLogger()

class DefaultPagination(pagination.LimitOffsetPagination):
    default_limit = 2
    # limit = 1
    # page_size = 2
    # max_page_size = 2
    # page_size_query_param = 'page_size'

class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    pagination_class = DefaultPagination

    @action(
        methods=['post'],
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
                data = {'detail': _('User in not authenticated')}
                return JsonResponse(data, status=status.HTTP_403_FORBIDDEN, safe=False)
            # Check session or csrf?
            if not session_key and not csrftoken:
                data = {'detail': _('Client session not found')}
                return JsonResponse(data, status=status.HTTP_403_FORBIDDEN, safe=False)

            favorite_tracks = request.user.favorite_tracks
            if value:
                favorite_tracks.add(pk)
            else:
                favorite_tracks.remove(pk)

            model = get_object_or_404(Track, pk=pk)
            data = {
                'played_count': model.played_count + 1,
            }
            serializer = TrackSerializer(model, data=data, partial=True, context={'request': request})

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data)
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
            csrftoken = request.headers.get('X-CSRFToken')

            # Check session or csrf?
            if not session_key and not csrftoken:
                return JsonResponse(
                    {
                        'detail': _('Client session not found'),
                    },
                    status=status.HTTP_403_FORBIDDEN,
                    safe=False,
                )

            model = get_object_or_404(Track, pk=pk)
            data = {
                'played_count': model.played_count + 1,
            }
            serializer = TrackSerializer(model, data=data, partial=True, context={'request': request})

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data)
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
