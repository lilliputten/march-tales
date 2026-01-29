import json
import logging
import traceback

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.helpers.errors import errorToString
from core.helpers.utils import debugObj

from ...models import Series, Track

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def update_series_tracks(request, series_id):
    """
    API endpoint to update series_order fields and remove tracks from a series.

    Expects JSON data in the format:
    {
        "tracks": [
            {"id": 1, "series_order": 1, "delete": false},
            {"id": 2, "series_order": 2, "delete": false},
            {"id": 3, "series_order": 3, "delete": true}
        ]
    }

    For tracks with delete=true, the series field will be set to None.
    For tracks with delete=false, the series_order will be updated.
    """
    # return JsonResponse({'error': 'Test error'}, status=500)
    try:
        # Get the series
        series = Series.objects.get(id=series_id)
    except Series.DoesNotExist:
        return JsonResponse({'error': 'Series not found'}, status=404)

    try:
        # Parse JSON data
        data = json.loads(request.body)
        tracks_data = data.get('tracks', [])
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    updated_tracks = []
    deleted_tracks = []

    for track_data in tracks_data:
        track_id = track_data.get('id')
        series_order = track_data.get('series_order')
        delete = track_data.get('delete', False)

        try:
            track = Track.objects.get(id=track_id)
        except Track.DoesNotExist:
            logger.warning(f'Track with id {track_id} not found')
            continue

        try:
            if delete:
                # Remove track from series
                track.series = None
                track.series_order = None
                track.save()
                deleted_tracks.append(track_id)
                logger.info(f'Removed track {track_id} from series {series_id}')
            elif series_order is not None and series_order:
                # Update series_order
                track.series = series
                track.series_order = series_order
                track.save()
                updated_tracks.append({'id': track_id, 'series_order': series_order})
                logger.info(f'Updated track {track_id} in series {series_id} with order {series_order}')
        except Exception as err:
            sError = errorToString(err)
            sTraceback = str(traceback.format_exc())
            debugData = {
                'error': sError,
                'traceback': sTraceback,
            }
            logger.error(f'[update_series_tracks]: Error processing data:\n{debugObj(debugData)}')
            return JsonResponse(debugData, status=500)

    return JsonResponse(
        {
            'success': True,
            'updated_tracks': updated_tracks,
            'deleted_tracks': deleted_tracks,
            'message': f'Updated {len(updated_tracks)} tracks and deleted {len(deleted_tracks)} tracks from series',
        }
    )
