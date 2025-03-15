import traceback

from django.db.models.query import Q
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
            predefined_order_values['-published'],
            predefined_order_values['title'],
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
        logger.error(f'[get_track_order_args]: Error getting order by arguments:\n{debugObj(debugData)}')
        raise err


def get_track_filter_kwargs(request: Request):
    """
    Possible filters' examples:

    - filter=author_id:1 - Get tracks for particular author id
    - filter=track_status:PUBLISHED filter=status:PUBLISHED filter=published -- Only published tracks (default and always presented filter)
    - filter=ids:2,5 filter=id__in:2,5 -- Limit results by those track indices
    """
    try:
        language = get_current_language()
        predefined_filter_entries = {
            'published': {'track_status': 'PUBLISHED'},
        }
        predefined_filter_keys = {
            'title': f'title_{language}',
            'status': 'track_status',
            'ids': 'id__in',
        }
        predefined_filter_values = {}
        # Store results
        kwargs: dict[str, any] = {
            # Use published filter always
            **predefined_filter_entries['published'],
        }
        filter = request.query_params.getlist('filter')
        if filter and len(filter):
            logger.info(f'[track_filters:get_track_filter_kwargs] filter={filter}')
            for value in filter:
                pair = value.split(filter_delimiter)
                if pair and len(pair) == 2:
                    k = pair[0]
                    if k in predefined_filter_keys:
                        k = predefined_filter_keys[k]
                    x = pair[1]
                    if x in predefined_filter_values:
                        x = predefined_filter_values[x]
                    if k == 'id__in':
                        x = list(map(lambda s: int(s), x.split(',')))
                    kwargs[k] = x
                else:
                    if value in predefined_filter_entries:
                        kwargs = {**kwargs, **predefined_filter_entries[value]}
                    else:
                        raise Exception(f'Error parsing filter entry: "{value}"')
        return kwargs
    except Exception as err:
        # sError = errorToString(err)
        sTraceback = str(traceback.format_exc())
        debugData = {
            'err': err,
            'traceback': sTraceback,
        }
        logger.error(f'[get_track_filter_kwargs] Error getting filter arguments:\n{debugObj(debugData)}')
        raise err


def get_search_filter_args(request: Request):
    """
    Checks only for `search` parameters and adds values = the existed args map:

    - search=The%20legend
    """
    try:
        # language = get_current_language()
        # Check if has `search` parameter
        search = request.query_params.get('search')
        args = []
        if search:
            logger.info(f'[track_filters:get_track_filter_kwargs] search={search}')
            # query = Q(**{f'title_{language}__icontains': search})
            query = Q(**{f'title_ru__icontains': search}) | Q(**{f'title_en__icontains': search})
            args.append(query)
            # kwargs[f'title_{language}__icontains'] = search
        return args
    except Exception as err:
        # sError = errorToString(err)
        sTraceback = str(traceback.format_exc())
        debugData = {
            'err': err,
            'traceback': sTraceback,
        }
        logger.error(f'Error parsing search arguments:\n{debugObj(debugData)}')
        raise err


__all__ = [
    'DefaultPagination',
    'get_track_order_args',
    'get_track_filter_kwargs',
]
