import json
import traceback
from datetime import datetime

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from core.helpers.errors import errorToString
from core.helpers.utils import debugObj
from core.logging import getDebugLogger
from tales_django.core.helpers.check_csrf import check_csrf
from tales_django.entities.Tracks.api.user_track_serializers import UserTrackSerializer
from tales_django.entities.Tracks.models import UserTrack

logger = getDebugLogger()


def update_user_track(json: dict, request: WSGIRequest) -> UserTrack:
    user_id: int = request.user.id
    if user_id is None or not user_id:
        raise Exception('User id is not defined')
    track_id: int = json['track_id']
    if track_id is None or not track_id:
        raise Exception('Track id is not defined')
    found = UserTrack.objects.get_or_create(user_id=user_id, track_id=track_id)
    obj: UserTrack = found[0]
    created: bool = found[1]
    debugData = {
        'obj': obj,
        'created': created,
        'track_id': track_id,
        'user_id': user_id,
        'json': json,
    }
    debugStr = debugObj(debugData)
    logger.info(f'[update_user_track] Got data\n{debugStr}')

    # now = timezone.now()   # datetime.datetime.now()
    updated = False

    # # json data example:
    # 'track_id' = 6
    # 'is_favorite' = True
    # 'played_count' = 0
    # 'position' = 0
    # 'favorited_at_sec' = 1744543724
    # 'played_at_sec' = 0
    # 'updated_at_sec' = 1744543724

    if json['favorited_at_sec'] is not None and json['favorited_at_sec']:
        favorited_at = timezone.make_aware(datetime.fromtimestamp(json['favorited_at_sec']))
        if obj.favorited_at is None or favorited_at.timestamp() > obj.favorited_at.timestamp():
            if json['is_favorite'] is not None and obj.is_favorite != json['is_favorite']:
                obj.is_favorite = json['is_favorite']
                obj.favorited_at = favorited_at
                updated = True

    if json['played_at_sec'] is not None and json['played_at_sec']:
        played_at = timezone.make_aware(datetime.fromtimestamp(json['played_at_sec']))
        if obj.played_at is None or played_at.timestamp() > obj.played_at.timestamp():
            if json['position'] is not None and obj.position != json['position']:
                obj.position = json['position']
                obj.played_at = played_at
                updated = True
            # if json['played_count'] is not None and obj.played_count != json['played_count']:
            #     obj.played_count = json['played_count']
            #     obj.played_at = played_at
            #     updated = True

    if updated:
        # obj.updated_at = now # This auto-update field
        obj.save()

    return obj


@csrf_exempt  # Will send json failure response manually
def sync_user_tracks_api_view(request: WSGIRequest):
    """
    Synchronize client tracks' data with server data.

    API url: `api/v1/user/tracks/sync/`
    See also: `tales_django/entities/Tracks/api/track_api_urlpatterns.py`
    """
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

        data = json.loads(request.body)

        items = data.get('items')

        if items is None or not isinstance(items, list):
            data = {'detail': _('Expected objects list')}
            return JsonResponse(
                data,
                status=status.HTTP_400_BAD_REQUEST,
                safe=False,
                json_dumps_params={'ensure_ascii': True},
                content_type='application/json; charset=utf-8',
            )

        debugData = {
            'items': items,
        }
        debugStr = debugObj(debugData)
        logger.info(f'[sync_user_tracks_api_view] Got data\n{debugStr}')

        # Sync all the UserTrack items...
        updated_items = map(lambda item: update_user_track(item, request), items)
        user_tracks_serializer = UserTrackSerializer(updated_items, read_only=True, many=True)

        data = {
            'updated_items': user_tracks_serializer.data,
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
