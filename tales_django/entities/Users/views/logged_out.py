from django.http import HttpRequest
from django.shortcuts import redirect, render

from core.helpers.utils import debugObj
from core.logging import getDebugLogger
from tales_django.core.pages import get_common_context, get_favorites_list_context, get_tracks_list_context

logger = getDebugLogger()


def logged_out(request: HttpRequest):
    mobile_auth = request.COOKIES.get('mobile_auth')

    context = {
        **get_common_context(request),
        **get_favorites_list_context(request),
        **get_tracks_list_context(request),
    }

    host = request.headers.get('Host')
    referer = request.headers.get('Referer')

    debugData = {
        'host': host,
        'referer': referer,
        'request': request,
        'cookies': request.COOKIES.get('cookies'),
        'mobile_auth': mobile_auth,
        'request.user': request.user,
        'context': context,
    }
    debugStr = debugObj(debugData)
    logger.info(f'logged_out\n{debugStr}')

    response = render(
        request=request,
        template_name='tales_django/logged_out.html.django',
        context=context,
    )
    return response
