import traceback
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework import permissions

from core.helpers.errors import errorToString
from core.logging import getDebugLogger

from .track_serializers import TrackSerializer

from ..models import Track

logger = getDebugLogger()


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    @action(detail=True, methods=['Get'])
    def show(self, _, pk=None):
        queryset = Track.objects.filter(pk=pk)
        serializer = TrackSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def toggleFavorite(self, request, pk=None):
        try:
            value = request.data.get('value')

            session = request.session
            session_key = session.session_key if session else None
            csrfToken = request.headers.get('X-CSRFToken')

            user = request.user

            # Check user is_authenticated?
            if not user.is_authenticated:
                data = {'detail': _('User in not authenticated')}
                return JsonResponse(data, status=status.HTTP_403_FORBIDDEN, safe=False)
            # Check session or csrf?
            if not session_key and not csrfToken:
                data = {'detail': _('Client session not found')}
                return JsonResponse(data, status=status.HTTP_403_FORBIDDEN, safe=False)

            # print('incrementPlayedCount', session, request, pk, played_count)

            favorite_tracks = user.favorite_tracks
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
            debug_data = {
                'err': err,
                'traceback': sTraceback,
            }
            logger.error('Caught error %s (re-raising): %s', sError, debug_data)
            # raise err
            return JsonResponse(
                {
                    'detail': sError,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                safe=False,
            )

    @action(methods=['post'], detail=True, permission_classes=[permissions.BasePermission])
    def incrementPlayedCount(self, request, pk=None):
        try:
            # played_count = request.data.get('played_count')

            session = request.session
            session_key = session.session_key if session else None
            csrfToken = request.headers.get('X-CSRFToken')

            # Check session or csrf?
            if not session_key and not csrfToken:
                return JsonResponse(
                    {
                        'detail': _('Client session not found'),
                    },
                    status=status.HTTP_403_FORBIDDEN,
                    safe=False,
                )

            # print('incrementPlayedCount', session, request, pk, played_count)

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
            debug_data = {
                'err': err,
                'traceback': sTraceback,
            }
            logger.error('Caught error %s (re-raising): %s', sError, debug_data)
            # raise err
            return JsonResponse(
                {
                    'detail': sError,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                safe=False,
            )
