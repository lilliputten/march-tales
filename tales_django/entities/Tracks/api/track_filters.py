import traceback

from django.utils.translation import gettext_lazy as _

from django.db.models.functions import Lower

from rest_framework.request import Request
from rest_framework import pagination

from core.helpers.utils import debugObj
from core.logging import getDebugLogger

from tales_django.core.model_helpers import get_current_language

from .track_constants import default_tracks_limit
from .common_constants import filter_delimiter

logger = getDebugLogger()


class DefaultPagination(pagination.LimitOffsetPagination):
    default_limit = default_tracks_limit


def get_track_order_args(request: Request):
    try:
        language = get_current_language()
        predefined_order_values = {
            'title': Lower(f'title_{language}'),
            '-title': Lower(f'title_{language}').desc(),
            'published': 'published_at',
            '-published': '-published_at',
        }
        default_order_args = [
            'published_at',
            Lower(f'title_{language}').desc(),
        ]
        order = request.query_params.getlist('order')
        if not order or not len(order):
            return default_order_args
        logger.info(f'[track_filters:get_track_order_args] order={order}')
        args = map(
            lambda x: predefined_order_values[x] if x in predefined_order_values else x,
            order,
        )
        args = list(args)
        return args
    except Exception as err:
        # sError = errorToString(err)
        sTraceback = str(traceback.format_exc())
        debugData = {
            'err': err,
            'traceback': sTraceback,
        }
        logger.error(f'Error getting order by arguments:\n{debugObj(debugData)}')
        raise err


def get_track_filter_kwargs(request: Request):
    try:
        language = get_current_language()
        predefined_filter_keys = {
            'title': f'title_{language}',
        }
        predefined_filter_values = {}
        default_filter_args = {
            'track_status': 'PUBLISHED',
        }
        filter = request.query_params.getlist('filter')
        if not filter or not len(filter):
            return default_filter_args
        logger.info(f'[track_filters:get_track_filter_kwargs] filter={filter}')
        args = {}
        for it in filter:
            pair = it.split(filter_delimiter)
            if not pair or len(pair) != 2:
                raise Exception(f'Error parsing filter pair: "{it}"')
            k = pair[0]
            if k in predefined_filter_keys:
                k = predefined_filter_keys[k]
            x = pair[1]
            if x in predefined_filter_values:
                x = predefined_filter_values[x]
            args[k] = x
        return args
    except Exception as err:
        # sError = errorToString(err)
        sTraceback = str(traceback.format_exc())
        debugData = {
            'err': err,
            'traceback': sTraceback,
        }
        logger.error(f'Error getting filter arguments:\n{debugObj(debugData)}')
        raise err


__all__ = [
    'DefaultPagination',
    'get_track_order_args',
    'get_track_filter_kwargs',
]
